import math
from collections import defaultdict
from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic.edit import (UpdateView)
from icecream import ic

from .forms import (TaskForm, CriterionFormSet, ItemFormSet)
from .models import *

SETTINGS_MAX_ITEMS_DEFAULT = 4
SETTINGS_MAX_CRITERIONS_DEAFULT = 4
types = {
    'task': Task,
    'criterion': Criterion,
    'item': Item,
    'cell': Cell,
    'param': ParamAUX,
    'descartes': CellDescartesCriterion,
    'descartes_item': CellDescartesItem,
}


def tasks(request):
    if not request.user.is_authenticated:
        return redirect('products:login_view')
    else:
        tasks = list()
        if request.user.is_active:
            if request.user.is_superuser:
                tasks = Task.objects.filter()
            else:
                tasks = Task.objects.filter(user=request.user)
        return render(request, "tasks/tasks.html", {'tasks': tasks})


def add_criterion(request, task_id):
    data = request.POST.dict()
    task = Task.objects.get(id=task_id)
    name = data['criterion-NONE-name']
    value, direction = 0, 0
    if name and len(Criterion.objects.filter(task=task)) < (Setting.objects.latest('id').max_criterions or SETTINGS_MAX_CRITERIONS_DEAFULT):
        new_criterion = Criterion.objects.create(task=task, name=name, value=float(value), direction=direction)
        for criterion_i in Criterion.objects.filter(task=task):
            for criterion_j in Criterion.objects.filter(task=task):
                try:
                    CellDescartesCriterion.objects.get(task=task, type='criterion', id_i=criterion_i.id, id_j=criterion_j.id)
                except:
                    CellDescartesCriterion.objects.create(task=task, type='criterion', id_i=criterion_i.id, id_j=criterion_j.id, value=1.0)
        for item_i in Item.objects.filter(task=task):
            for item_j in Item.objects.filter(task=task):
                try:
                    CellDescartesItem.objects.get(task=task, criterion=new_criterion, id_i=item_i.id, id_j=item_j.id)
                except:
                    CellDescartesItem.objects.create(task=task, criterion=new_criterion, id_i=item_i.id, id_j=item_j.id, value=1.0)
    return redirect('products:add_criteria', task_id=task_id)


def add_item(request, task_id):
    data = request.POST.dict()
    task = Task.objects.get(id=task_id)
    name = data['item-NONE-name']
    if name and len(Item.objects.filter(task=task)) < (Setting.objects.latest('id').max_items or SETTINGS_MAX_ITEMS_DEFAULT):
        new_item = Item.objects.create(task=task, name=name)
        for criterion in Criterion.objects.filter(task=task):

            for item_i in Item.objects.filter(task=task):
                for item_j in Item.objects.filter(task=task):
                    try:
                        CellDescartesItem.objects.get(task=task, criterion=criterion, id_i=item_i.id, id_j=item_j.id)
                    except:
                        CellDescartesItem.objects.create(task=task, criterion=criterion, id_i=item_i.id, id_j=item_j.id, value=1.0)
        for key, value in data.items():
            if 'cell-' in key and value:
                criterion_id = str(key).split('-')[1]
                criterion = Criterion.objects.get(id=criterion_id)
                Cell.objects.create(task=task, item=new_item, criterion=criterion, value=value)
    return redirect('products:add_items', task_id=task_id)


def update_criterion(request, pk):
    data = request.POST.dict()
    try:
        criterion = Criterion.objects.get(id=pk)
    except Criterion.DoesNotExist:
        messages.success(request, 'Object Does not exit')
        return redirect('products:update_task', pk=criterion.task.id)
    if 'submit-update' in data.keys():
        for key, value in data.items():
            if str(key).startswith('object-'):
                _update_object(key, value)
    if 'submit-delete-criterion' in data.keys():
        [cell.delete() for cell in CellDescartesCriterion.objects.filter(task=criterion.task, type='criterion', id_i=criterion.id)]
        [cell.delete() for cell in CellDescartesCriterion.objects.filter(task=criterion.task, type='criterion', id_j=criterion.id)]
        criterion.delete()
    return redirect('products:add_criteria', task_id=criterion.task.id)


class TaskInline:
    form_class = TaskForm
    model = Task
    template_name = "tasks/task_v4.html"

    def form_valid(self, form):
        ic('call form_valid()...')
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
        self.object = form.save()
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, f'formset_{name}_valid', None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('products:update_task', pk=self.object.pk)

    # def formset_items_valid(self, formset):
    #     items = formset.save(commit=False)
    #     for obj in formset.deleted_objects:
    #         obj.delete()
    #     for item in items:
    #         item.product = self.object
    #         item.save()
    #
    # def formset_variants_valid(self, formset):
    #     variants = formset.save(commit=False)
    #     for obj in formset.deleted_objects:
    #         obj.delete()
    #     for variant in variants:
    #         variant.product = self.object
    #         variant.save()


class TaskUpdate(TaskInline, UpdateView):

    def get_context_data(self, **kwargs):
        ic('call TaskUpdate()')
        ctx = super(TaskUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()

        task = get_object_or_404(Task, pk=self.object.pk)

        items = Item.objects.filter(task__pk=task.pk)
        criteria = Criterion.objects.filter(task__pk=task.pk)

        ctx['items'] = items
        ctx['criteria'] = criteria
        ctx['task_id'] = task.id

        cells = dict()
        for item in items:
            if item not in cells.keys():
                cells[item] = dict()
            for criterion in criteria:
                try:
                    cell = Cell.objects.get(task=task, item=item, criterion=criterion)
                except Cell.DoesNotExist:
                    cell = Cell.objects.create(task=task, item=item, criterion=criterion, value=0.0)
                cells[item][criterion] = cell
        ctx['cells'] = cells

        # for criterion_i in criteria:
        #     if criterion_i not in cells_descartes_criteria.keys():
        #         cells_descartes_criteria[criterion_i] = dict()
        #     for criterion_j in criteria:
        #         try:
        #             cell = CellDescartesCriterion.objects.get(task=task, type='criterion', id_i=criterion_i.id, id_j=criterion_j.id)
        #         except CellDescartesCriterion.DoesNotExist:
        #             cell = CellDescartesCriterion.objects.create(task=task, type='criterion', id_i=criterion_i.id, id_j=criterion_j.id, value=0)
        #         cells_descartes_criteria[criterion_i][criterion_j] = cell
        # cells_descartes_items = dict()
        # criteria = Criterion.objects.filter(task=task)
        # for criterion in criteria:
        #     if criterion not in cells_descartes_items.keys():
        #         cells_descartes_items[criterion] = dict()
        #     cells_descartes_items_inner = dict()
        #     for item_i in items:
        #         if item_i not in cells_descartes_items_inner.keys():
        #             cells_descartes_items_inner[item_i] = dict()
        #         for item_j in items:
        #             try:
        #                 cell = CellDescartesItem.objects.get(task=task, criterion=criterion, id_i=item_i.id, id_j=item_j.id)
        #             except CellDescartesItem.DoesNotExist:
        #                 cell = CellDescartesItem.objects.create(task=task, criterion=criterion, id_i=item_i.id, id_j=item_j.id, value=0)
        #             cells_descartes_items_inner[item_i][item_j] = cell
        #     cells_descartes_items[criterion] = cells_descartes_items_inner
        # ctx['cells_descartes_items'] = cells_descartes_items
        #

        cells_descartes_criteria = dict()
        for criterion_i in criteria:
            if criterion_i not in cells_descartes_criteria.keys():
                cells_descartes_criteria[criterion_i] = dict()
            for criterion_j in criteria:
                # ic(task, criterion_i.id, criterion_j.id)
                cells_descartes_criteria[criterion_i][criterion_j] = CellDescartesCriterion.objects.get(task=task, id_i=criterion_i.id, id_j=criterion_j.id)
        ctx['cells_descartes_criteria'] = cells_descartes_criteria

        cells_descartes_items = dict()
        criteria = Criterion.objects.filter(task=task)
        for criterion in criteria:
            if criterion not in cells_descartes_items.keys():
                cells_descartes_items[criterion] = dict()
            cells_descartes_items_inner = dict()
            for item_i in items:
                if item_i not in cells_descartes_items_inner.keys():
                    cells_descartes_items_inner[item_i] = dict()
                for item_j in items:
                    # ic(task, criterion, item_i.id, item_j.id)
                    cells_descartes_items_inner[item_i][item_j] = CellDescartesItem.objects.get(task=task, criterion=criterion, id_i=item_i.id, id_j=item_j.id)
            cells_descartes_items[criterion] = cells_descartes_items_inner
        ctx['cells_descartes_items'] = cells_descartes_items

        ctx['task_result'] = task.result
        ctx['can_add_criteria'] = len(Criterion.objects.filter(task=task)) < (Setting.objects.latest('id').max_criterions or SETTINGS_MAX_CRITERIONS_DEAFULT)
        ctx['can_add_items'] = len(Item.objects.filter(task=task)) < (Setting.objects.latest('id').max_items or SETTINGS_MAX_ITEMS_DEFAULT)

        show_criterion_weight = False
        show_criterion_direction = False
        show_need_descartes_criterion = False
        show_need_descartes_item = False
        for method in task.methods.all():
            show_criterion_weight += method.need_criterion_weight
            show_criterion_direction += method.need_criterion_direction
            show_need_descartes_criterion += method.need_descartes_criterion
            show_need_descartes_item += method.need_descartes_item

            if method.need_criterion_weight:
                sum = 0
                for criterion in criteria:
                    sum += criterion.value
                if sum != 1:
                    ctx['error_criteria_value_sum'] = 'Сумма вероятностей должна быть равна 1!'
        ctx['show_criterion_weight'] = show_criterion_weight
        ctx['show_criterion_direction'] = show_criterion_direction
        ctx['show_need_descartes_criterion'] = show_need_descartes_criterion
        ctx['show_need_descartes_item'] = show_need_descartes_item
        # for crit, crits in ctx['cells_descartes_criteria'].items():
        #     for c in crits:
        #         ic(crit, c.value)
        return ctx

    def get_named_formsets(self):
        post = self.request.POST or None
        files = self.request.FILES or None
        return {
            'criteria': CriterionFormSet(post, files, instance=self.object, prefix='criteria'),
            'items': ItemFormSet(post, files, instance=self.object, prefix='items'),
        }


def _update_object(key: str, value):
    _, obj_type, obj_id, obj_field = key.split('-')
    if obj_id != 'NONE':
        obj = types[obj_type].objects.get(id=obj_id)
        old_value = str(getattr(obj, obj_field))
        if old_value != value:
            setattr(obj, obj_field, value)
            obj.save()


def test(request):
    # print(request.POST.dict())
    if request.method == 'POST':
        fruits = request.POST.getlist('fruits')
        # print(fruits)


def update_task_v2(request, task_id):
    # ic('update_task_v2')
    data = request.POST.dict()
    # ic(data)
    for key, value in data.items():
        obj_img = None
        if str(key).startswith('object-'):
            _, obj_type, obj_id, obj_field = key.split('-')
            if obj_id != 'NONE':
                obj = types[obj_type].objects.get(id=obj_id)
                old_value = str(getattr(obj, obj_field))
                if old_value != value:
                    # ic(_, obj_type, obj_id, obj_field, old_value, value)
                    setattr(obj, obj_field, value)
                    setattr(obj, 'changed', True)
                    obj.save()
                    if obj_type in ['descartes', 'descartes_item']:
                        if obj.id_i == obj.id_j:
                            setattr(obj, 'value', 1)
                            setattr(obj, 'changed', True)
                            obj.save()
                        else:
                            if obj_type == 'descartes':
                                obj_img = CellDescartesCriterion.objects.get(task=obj.task, id_i=obj.id_j, id_j=obj.id_i)
                            if obj_type == 'descartes_item':
                                obj_img = CellDescartesItem.objects.get(task=obj.task, criterion=obj.criterion, id_i=obj.id_j, id_j=obj.id_i)
                            value_img = 1.0 / float(obj.value)  # TODO: DIVIDE BY ZERO ISSUE
                            setattr(obj_img, 'value', value_img)
                            obj_img.save()
                        obj.save()
                        if obj_img:
                            obj_img.changed = True
                            obj_img.save()
                    break
    return redirect('products:task', pk=task_id)


def add_task(request):
    last_task_id = Task.objects.latest('id').id or 0
    task_name = f'Task_{last_task_id}'
    ctx = {'task_name': task_name}
    return render(request, "tasks/add_task.html", ctx)


def set_task_name(request):
    data = request.POST.dict()
    task_name = data['task_name'] or str()
    if not task_name:
        ctx = {'task_name': task_name, 'error_message': 'Введите название задачи!'}
        return render(request, "tasks/add_task.html", ctx)
    return redirect('products:get_answer', task_name=task_name, question_id=1)


def get_answer(request, task_name, question_id=1):
    data = request.POST.dict()
    question, methods = Question.objects.get(id=question_id), None
    ctx = {"task_name": task_name, "question": question, 'methods': methods}
    if data.items():
        if 'choice' not in data.keys():
            ctx['error_message'] = 'Выберите вариант!'
            return render(request, "tasks/wizard.html", ctx)
        else:
            choice = Choice.objects.get(id=data['choice'])
        if choice.next_question:
            ctx['question'] = Question.objects.get(id=choice.next_question.id)
            return render(request, "tasks/wizard.html", ctx)
        else:
            methods = choice.methods.all()
    ctx['question'] = get_object_or_404(Question, pk=question_id)
    ctx['methods'] = methods
    return render(request, "tasks/wizard.html", ctx)


def add_criteria(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    criteria = Criterion.objects.filter(task__pk=task.pk)
    ctx = {'task_id': task_id, 'criteria': criteria, 'can_add_criteria': len(criteria) < (Setting.objects.latest('id').max_criterions or SETTINGS_MAX_CRITERIONS_DEAFULT)}
    return render(request, "tasks/add_criteria.html", ctx)


def add_items(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    items = Item.objects.filter(task__pk=task.pk)
    ctx = {'task_id': task_id, 'items': items, 'can_add_items': len(items) < (Setting.objects.latest('id').max_items or SETTINGS_MAX_ITEMS_DEFAULT)}
    return render(request, "tasks/add_items.html", ctx)


def update_item(request, pk):
    data = request.POST.dict()
    try:
        item = Item.objects.get(id=pk)
    except Item.DoesNotExist:
        messages.success(request, 'Object Does not exit')
        return redirect('products:update_task', pk=item.task.id)
    if 'submit-update-' in data.keys():
        name = data['name']
        if name:
            item.name = name
            item.save()
        # print(request.POST.getlist('cell'))
        for key, value in data.items():
            if str(key).startswith('object-'):
                _update_object(key, value)
    if 'submit-update' in data.keys():
        # print(request.POST.getlist('cell'))
        for key, value in data.items():
            if str(key).startswith('object-'):
                _update_object(key, value)
    if 'submit-delete-item' in data.keys():
        criteria = Criterion.objects.filter(task=item.task)
        for criterion in criteria:
            [cell.delete() for cell in CellDescartesItem.objects.filter(task=item.task, criterion=criterion, id_i=item.id)]
            [cell.delete() for cell in CellDescartesItem.objects.filter(task=item.task, criterion=criterion, id_j=item.id)]
        item.delete()
    return redirect('products:add_items', task_id=item.task.id)


def create_task(request, task_name):
    task = Task.objects.create(user=request.user, name=task_name)
    method_ids = request.POST.getlist('method')
    task.methods.set(method_ids)
    params = list()
    for method_id in method_ids:
        params.extend(Method.objects.get(id=method_id).params.all())
    for param in list(dict.fromkeys(params)):
        ParamAUX.objects.create(task=task, param=param, value=0)
    return redirect('products:task', pk=task.id)


def execute(request, pk):
    task = Task.objects.get(pk=pk)
    return execute_logic(task=task)


def transpose(dct):
    d = defaultdict(dict)
    for key1, inner in dct.items():
        for key2, value in inner.items():
            d[key2][key1] = value
            # d[key1][key2] = value
    return d


def _get_table_by_item(task: Task):
    cells = Cell.objects.filter(task=task)
    table = dict()
    for cell in cells:
        if cell.item not in table.keys():
            table[cell.item] = dict()
        table[cell.item][cell.criterion] = float(cell.value)
    return table


def _get_table_criteria_descartes(task: Task):
    cells = CellDescartesCriterion.objects.filter(task=task)
    table = dict()
    for cell in cells:
        if cell.id_i not in table.keys():
            table[cell.id_i] = dict()
        table[cell.id_i][cell.id_j] = float(cell.value)
    return table


def _get_table_items_descartes(task: Task):
    items = CellDescartesItem.objects.filter(task=task)
    temp = dict()
    for item in items:
        if item.criterion not in temp.keys():
            temp[item.criterion] = list()
        temp[item.criterion].append(item)
    # ic(temp)
    table = dict()
    for criterion, cells in temp.items():
        inner = dict()
        for cell in cells:
            if cell.id_i not in inner.keys():
                inner[cell.id_i] = dict()
            inner[cell.id_i][cell.id_j] = float(cell.value)
        # ic(inner)
        table[criterion] = inner
    return table


def _get_params(task: Task):
    return {param_aux.param.name: param_aux.value for param_aux in task.paramaux_set.all()}


def _get_param(task: Task, name: str):
    params = _get_params(task)
    value = params.get(name, 0)
    return value


def login_view(request):
    # ic(request)
    if request.method == "POST":
        # ic(request.POST)
        return redirect('products:list_tasks')
    else:
        # ic(request.GET)
        return render(request, "login.html")


def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    # return render(request, "login.html")
    return redirect('products:login_view')


class Executor:
    def get_max(self, objects: dict):
        return max(list(objects.items()), key=lambda i: i[1])

    def get_min(self, objects: dict):
        return min(list(objects.items()), key=lambda i: i[1])

    def _normalize(self, task: Task):
        table_by_item = _get_table_by_item(task)
        table_by_criterion = transpose(table_by_item)
        rj_max, rj_min, rj_diff = dict(), dict(), dict()
        for criterion, cells in table_by_criterion.items():
            for item, cell_value in cells.items():
                min_item, min_value = self.get_min(cells)
                max_item, max_value = self.get_max(cells)
                rj_max[criterion] = max_value
                rj_min[criterion] = min_value
                rj_diff[criterion] = max_value - min_value
                # ic(criterion.name, item.name, cell_value)
        # ic(rj_max, rj_min, rj_diff)
        table_by_item_normalized = _get_table_by_item(task)
        for item, cells in table_by_item.items():
            for criterion, cell_value in cells.items():
                normalize_value = 0
                if rj_diff[criterion] != 0:
                    if criterion.direction_bool == 0:
                        normalize_value = (table_by_criterion[criterion][item] - rj_min[criterion]) / rj_diff[criterion]  # TODO: DIVIDE BY ZERO ISSUE
                    else:
                        normalize_value = (rj_max[criterion] - table_by_criterion[criterion][item]) / rj_diff[criterion]  # TODO: DIVIDE BY ZERO ISSUE
                    # ic(criterion, criterion.direction_bool, normalize_value)
                table_by_item_normalized[item][criterion] = normalize_value
        return table_by_item_normalized

    def zmm(self, task: Task):
        table = _get_table_by_item(task)
        eir = dict()
        for item, cells in table.items():
            eir[item] = min([float(v) for k, v in cells.items()])
            # temp_minimums[item] = self.get_min(cells)
        # result, value = min(list(temp_minimums.items()), key=lambda i: i[1])
        # ic(eir)
        result, value = self.get_max(eir)
        # ic(result, value)
        return result

    def maxmax(self, task: Task):
        table = _get_table_by_item(task)
        eir = dict()
        for item, cells in table.items():
            eir[item] = max([float(v) for k, v in cells.items()])
            # temp_maximus[item] = self.get_max(cells)
        # result, value = max(list(temp_maximus.items()), key=lambda i: i[1])
        # ic(eir)
        result, value = self.get_max(eir)
        # ic(result, value)
        return result

    def zbl(self, task: Task):
        table = _get_table_by_item(task)
        zbl = dict()
        for item, cells in table.items():
            sum_bl = 0
            for criterion, cell_value in cells.items():
                sum_bl += cell_value * criterion.value
            zbl[item] = sum_bl
        # ic(zbl)
        result, value = self.get_max(zbl)
        # ic(result, value)
        return result

    def zs(self, task: Task):
        table = _get_table_by_item(task)
        criterions = Criterion.objects.filter(task=task)
        max_criterions = dict()
        min_criterions = dict()
        for criterion in criterions:
            cells = Cell.objects.filter(task=task, criterion=criterion)
            max_criterions[criterion] = max([cell.value for cell in cells])
            min_criterions[criterion] = min([cell.value for cell in cells])
        cells = Cell.objects.filter(task=task)
        table_savige = dict()
        for cell in cells:
            if cell.item not in table_savige.keys():
                table_savige[cell.item] = dict()
            table_savige[cell.item][cell.criterion] = max_criterions[cell.criterion] - float(cell.value)
        # for key, value in table_savige.items():
        #     ic(key, value)
        eir = dict()
        for item, cells in table_savige.items():
            values = [float(v) for k, v in cells.items()]
            eir[item] = max(values)
        # ic(eir)
        result, value = self.get_min(eir)
        # ic(result, value)
        return result

    def zhw(self, task: Task):
        table = _get_table_by_item(task)
        c = _get_param(task, 'c')
        eir = dict()
        for item, cells in table.items():
            item_max, item_max_value = self.get_max(cells)
            item_min, item_min_value = self.get_min(cells)
            eir[item] = c * item_min_value + (1 - c) * item_max_value
        # ic(eir)
        result, value = self.get_max(eir)
        # ic(result, value)
        return result

    def zhl(self, task: Task):
        table = _get_table_by_item(task)
        v = _get_param(task, 'v')
        temp = dict()
        for item, cells in table.items():
            min_item, min_value = self.get_min(cells)
            sum_bl = 0
            for criterion, cell_value in cells.items():
                sum_bl += cell_value * criterion.value
            temp[item] = v * sum_bl + (1 - v) * min_value
        result, value = self.get_max(temp)
        # ic(result, value)
        return result

    def zg(self, task: Task):
        table = _get_table_by_item(task)
        zg = dict()
        temp = dict()
        for item, cells in table.items():
            temp[item] = list()
            for criterion, cell_value in cells.items():
                multiple = cell_value * criterion.value
                temp[item].append(multiple)
            minimum = min(temp[item])
            zg[item] = minimum
        # ic(zg)
        result, value = self.get_max(zg)
        # ic(result, value)
        return result

    def blmm(self, task: Task):
        table = _get_table_by_item(task)
        z = _get_param(task, 'z')
        mm = dict()
        table_aux = dict()
        for item, cells in table.items():
            table_aux[item] = dict()
            mm_object, mm_value = self.get_min(cells)
            max_object, max_value = self.get_max(cells)
            table_aux[item]['max'] = max_value
            mm[item] = mm_value
            table_aux[item]['mm'] = mm_value
            math_expected = 0
            for criterion, cell_value in cells.items():
                math_expected += cell_value * criterion.value
            table_aux[item]['math_expected'] = math_expected
            # ic(item, math_expected)
            max_object, max_value = self.get_max(cells)
            table_aux[item]['max'] = max_value
        opora_obj, opora_value = self.get_max(mm)

        for item, cells in table.items():
            if table_aux[item]['mm'] == opora_value:
                obj, max_by_opora = self.get_max(cells)
                table_aux[item]['max_by_opora'] = max_by_opora
                # ic(item, max_by_opora)
            table_aux[item]['risk'] = opora_value - table_aux[item]['mm']

        for item, cells in table.items():
            if opora_value == table_aux[item]['mm']:
                obj, max_for_win = self.get_max(cells)
                break
        eoptim = dict()
        for item, cells in table.items():
            winner = table_aux[item]['max'] - max_for_win
            if table_aux[item]['risk'] <= z and table_aux[item]['risk'] <= winner:
                table_aux[item]['eoptim'] = table_aux[item]['math_expected']
                eoptim[item] = table_aux[item]['math_expected']
            else:
                table_aux[item]['eoptim'] = 0
                eoptim[item] = 0
        result, value = self.get_max(eoptim)
        return result

    def ideal(self, task: Task):
        ideal = dict()
        table_normalized = self._normalize(task)
        for item, cells in table_normalized.items():
            pi = 0
            for criterion, cell_value in cells.items():
                pi += (table_normalized[item][criterion] ** 2) * criterion.value
            ideal[item] = math.sqrt(pi)
            # ic(item, ideal[item])
        result, value = self.get_min(ideal)
        return result

    def compromise(self, task: Task):
        compromise = dict()
        table_normalized = self._normalize(task)
        for item, cells in table_normalized.items():
            pi = 1
            for criterion, cell_value in cells.items():
                pi *= table_normalized[item][criterion] * criterion.value
            compromise[item] = pi
            # ic(item, compromise[item])
        result, value = self.get_max(compromise)
        return result

    def _mai_algo(self, table_descartes: dict):
        table_descartes_trans = transpose(table_descartes)
        # ic(table_descartes)

        len_criteria = len(table_descartes.keys()) or 0
        # ic(len_criteria)
        crit_count = Decimal(len_criteria)
        # ic(crit_count)
        table_1 = dict()
        sum_root_5 = 0
        for criterion_i, criterions in table_descartes.items():
            p = Decimal(1)
            for criterion_j, value in criterions.items():
                p *= Decimal(value)
            root5 = Decimal(math.pow(p, Decimal(1) / crit_count))  # TODO: DIVIDE BY ZERO ISSUE
            sum_root_5 += root5
            table_1[criterion_i] = {'p': p, 'root5': root5}
        # ic(sum_root_5)

        for criterion, values in table_1.items():
            sum_root_5 = 1 if sum_root_5 == 0 else sum_root_5
            table_1[criterion]['nvp'] = Decimal(table_1[criterion]['root5']) / sum_root_5  # TODO: DIVIDE BY ZERO ISSUE

        l = Decimal(0)
        table_sum = dict()
        for criterion_j, criterions in table_descartes_trans.items():
            sum = Decimal(0)
            for criterion_i, value in criterions.items():
                sum += Decimal(value)
            table_sum[criterion_j] = sum
            l += sum * Decimal(table_1[criterion_j]['nvp'])

        try:
            control_is = (l - crit_count) / (crit_count - 1)  # TODO: DIVIDE BY ZERO ISSUE
        except Exception:
            control_is = 0

        k = {
            1: 0,
            2: 0,
            3: 0.58,
            4: 0.9,
            5: 1.12,
            6: 1.24,
            7: 1.32,
            8: 1.41,
            9: 1.45,
            10: 1.29,
        }
        ic(crit_count, k[crit_count])
        d = k[crit_count]
        control_os = control_is / Decimal(d)
        execute_result = {
            'table_1': table_1,
            'table_sum': table_sum,
            'sum_root_5': sum_root_5,
            'l': l,
            'crit_count': crit_count,
            'control_is': control_is,
            'control_os': control_os,
        }
        return execute_result

    def mai(self, task: Task):
        mai = dict()

        table_descartes = _get_table_criteria_descartes(task)

        criterion_result = self._mai_algo(table_descartes)
        # ic(criterion_result)

        # ic(table_1)
        # ic(table_sum)
        # ic(sum_root_5)
        # ic(l)
        # ic(crit_count)
        # ic(control_is)
        # ic(control_os)

        table_result = dict()
        tables_of_items = _get_table_items_descartes(task)
        # ic(tables_of_items)
        for criterion, table in tables_of_items.items():
            execute_result = self._mai_algo(table)
            # ic(criterion, execute_result)
            if criterion not in table_result.keys():
                table_result[criterion] = dict()
                for item_id, values in execute_result['table_1'].items():
                    item = Item.objects.get(id=item_id)
                    table_result[criterion][item] = values['nvp']
        table_result = transpose(table_result)
        # ic(table_result)

        table_final = dict()
        for item, criterions in table_result.items():
            nvp_final = 0
            for criterion, values in criterions.items():
                nvp_final += criterion_result['table_1'][criterion.id]['nvp'] * values
                # ic(criterion_result['table_1'])
            table_final[item] = nvp_final
        ic(table_final)
        result, value = self.get_max(table_final)
        return result

    def default(self, task: Task):
        table = _get_table_by_item(task)
        params = _get_params(task)
        # print(params)
        return None


execute_methods = {
    'ZMM': Executor().zmm,
    'ZHW': Executor().zhw,
    'ZBL': Executor().zbl,
    'ZHL': Executor().zhl,
    'ZS': Executor().zs,
    'ZG': Executor().zg,
    'maxmax': Executor().maxmax,
    'blmm': Executor().blmm,

    'IDEAL': Executor().ideal,
    'compromise': Executor().compromise,

    'MAI': Executor().mai,

    'ZBLn': Executor().default,
    'FUZZY': Executor().default,
    'ELECTRE': Executor().default,
    'ZBLMM': Executor().default,
}


def execute_logic(task: Task):
    result = dict()
    # result[Method.objects.get(name_short='ZMM').name] = Executor().zmm(task=task)
    # result['МАКСИМАКСНЫЙ'] = max(temp_maximus, key=temp_maximus.get)
    # result[Method.objects.get(name_short='ZS').name] = Executor().zs(task=task)
    # result[Method.objects.get(name_short='ZBL').name] = Executor().zbl(task=task)
    # result['__ГУРВИЦА__'] = Executor().zhw(task=task)

    results_task = Result.objects.filter(task=task)
    # ic(len(results_task))
    [result.delete() for result in results_task]
    for method in task.methods.all():
        ic(method)
        if method.name_short in execute_methods.keys():
            item = execute_methods[method.name_short](task=task)
            if item:
                Result(task=task, method=method, item=item).save()
                result[method.name] = item.name

    # Making all cells unchanged
    cells = list()
    cells.extend(Cell.objects.filter(task=task))
    cells.extend(CellDescartesCriterion.objects.filter(task=task))
    cells.extend(CellDescartesItem.objects.filter(task=task))
    cells.extend(Criterion.objects.filter(task=task))
    cells.extend(ParamAUX.objects.filter(task=task))
    for cell in cells:
        cell.changed = False
        cell.save()

    import json
    task.result = json.dumps(result)
    task.result = result
    task.save()
    return redirect('products:task', pk=task.pk)


def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('products:list_tasks')
