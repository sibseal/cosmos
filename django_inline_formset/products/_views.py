'''

    print(request.POST.dict().items())
    for key, value in request.POST.dict().items():
        print(f'KEY={key}')
        if key == 'submit-add-criterion':
            criterion = Criterion(task=task, name=f'Новое условие', value=0)
            criterion.save()
            return redirect('products:update_task', pk=pk)
        if key == 'submit-add-item':
            item = Item(task=task, name='new task')
            item.save()
            return redirect('products:update_task', pk=pk)
        if key == 'submit-execute':
            pass
        if key not in ['csrfmiddlewaretoken', 'user', 'submit-execute', 'submit-add-criterion', 'submit-add-item']:
            print(key)
            item_type, item_id, item_field = [str(i) for i in key.split("-")]
            print(item_type, item_id, item_field, value)
            types = {
                'tasks': Task,
                'criterions': Criterion,
                'items': Item,
                'cells': Cell
            }
            if item_id != 'NONE':
                item = types[item_type].objects.get(id=item_id)
                old_value = str(getattr(item, item_field))
                if old_value != value:
                    setattr(item, item_field, value)
                    item.save()
            return redirect('products:update_task', pk=pk)
        if key == 'submit-execute':
            return execute_logic(task=task)

def delete_criterion(request, pk):
    try:
        criterion = Criterion.objects.get(id=pk)
    except Criterion.DoesNotExist:
        messages.success(request, 'Object Does not exit')
        return redirect('products:update_task', pk=criterion.task.id)
    criterion.delete()
    return redirect('products:add_criteria', pk=criterion.task.id)
def delete_item(request, pk):
    try:
        item = Item.objects.get(id=pk)
    except Item.DoesNotExist:
        messages.success(request, 'Object Does not exit')
        return redirect('products:update_task', pk=item.task.id)
    item.delete()
    return redirect('products:add_items', pk=item.task.id)

'''


'''
<form action="{% url 'products:update_task_v2' task_id %}" method="post" id="descartesForm">
    {% csrf_token %}
    <input type="hidden" name="type" value="criterion"/>
    <table>
        <tr>
            <th>Критерий A</th>
            <th>Значение</th>
            <th>Критерий B</th>
        </tr>
        <tr>
            <td>
                <select name="id_i">
                    {% for criterion in criteria %}
                    <option value="{{ criterion.id }}">{{ criterion.name }}</option>
                    {% endfor %}
                </select>
            </td>
            <td><input name="value" type="range" min="-5" max="5" value="0" onchange="this.form.submit()"></td>
            <td>
                <select name="id_j">
                    {% for criterion in criteria %}
                    <option value="{{ criterion.id }}">{{ criterion.name }}</option>
                    {% endfor %}
                </select>
            </td>
        </tr>
        <tr>
            <td></td>
            <td>
                <output id="output_value" style="text-align:center;"></output>
            </td>
            <td></td>
        </tr>
    </table>
    <input type="submit" value="Vote"/>
</form>

'''

'''
<script>
    let i = document.getElementById('slider');
    let o = document.getElementById('output_value');
    o.innerHTML = i.value;
    i.addEventListener('input', function () {
        o.innerHTML = i.value;
    }, false);


    let descartesForm = document.getElementById("descartesForm");

    descartesForm.addEventListener("submit", (e) => {
        e.preventDefault();
    });
<!--    descartesForm.submit()-->

</script>

'''

'''


def update_task_v2_(request, task_id):
    ic('update_task_v2')
    data = request.POST.dict()
    ic(data)
    for key, value in data.items():
        if str(key).startswith('object-'):
            _update_object(key, value)
    return redirect('products:update_task', pk=task_id)

'''

'''
# def get_value(request, pk):
#     print(request.POST)
#     task = Task.objects.get(pk=pk)
#     return redirect('products:update_task', pk=task.pk)

'''

'''
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
        [cell.delete() for cell in CellD.objects.filter(task=criterion.task, type='criterion', id_i=criterion.id)]
        [cell.delete() for cell in CellD.objects.filter(task=criterion.task, type='criterion', id_j=criterion.id)]
        criterion.delete()
    return redirect('products:add_criteria', task_id=criterion.task.id)

'''

'''
<!--                                                <input type="number"-->
<!--                                                       id="object-criterion-{{ criterion.id }}-direction"-->
<!--                                                       name="object-criterion-{{ criterion.id }}-direction"-->
<!--                                                       class="form-control" min="0" max="1"-->
<!--                                                       value="{{criterion.direction}}"-->
<!--                                                       onchange="this.form.submit()"-->
<!--                                                       step="1"-->
<!--                                                />-->

                <!--                                                       value="{{criterion.direction_bool}}"-->
<!--                                            name="object-criterion-{{ criterion.id }}-direction_bool"-->
<!--                                                <input type="checkbox"-->
<!--                                                       id="object-criterion-{{ criterion.id }}-direction_bool"-->
<!--                                                       name="direction_bool"-->
<!--                                                       class="form-check-input mt-0 align-middle"-->
<!--                                                       onchange="this.form.submit()"-->
<!--                                                       {% if criterion.direction_bool %} checked {% endif %}-->
<!--                                                />{{criterion.direction_bool}} {{ criterion.direction_bool }}-->

'''

'''
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

'''