from django.contrib import admin

from .models import *


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 0
    fk_name = "question"


class ParamAUXInLine(admin.StackedInline):
    model = ParamAUX
    extra = 0


class TaskAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'name', 'methods', 'enable_normalization','use_normalized']}),
    ]

    inlines = [ItemInline, ParamAUXInLine]
    list_display = ('name',)
    list_filter = ['name']
    search_fields = ['name']

    list_display = ('user', 'name')

    def pretty(self, d, indent=0):
        for key, value in d.items():
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                self.pretty(value, indent + 1)
            else:
                print('\t' * (indent + 1) + str(value))

    def render_change_form(self, request, context, *args, **kwargs):
        print('render_change_form')
        print(self.pretty(context))
        print(context['adminform'].form.fields)
        # context['adminform'].form.fields['theme'].queryset = ParamAUX.objects.filter(param='company')
        return super(TaskAdmin, self).render_change_form(request, context, *args, **kwargs)


class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['task', 'name', 'name_short']}),
    ]
    list_display = ('task', 'name', 'name_short')


class CriterionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['task', 'name', 'name_short', 'value', 'direction_bool','normalize_param_p','normalize_param_k']}),
    ]
    list_display = ('id', 'task', 'name', 'name_short')


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'choice_text', 'next_question')


class MethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_short', 'name')


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ['step', "question_text", 'description']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('id', 'step', 'question_text', 'description')


class SettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'max_items', 'max_criterions')


class ParamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


class CellDescartesCriterionAdmin(admin.ModelAdmin):
    list_display = ('id','task', 'type', 'id_i', 'id_j', 'value')


class CellDescartesItemAdmin(admin.ModelAdmin):
    list_display = ('task', 'criterion', 'id_i', 'id_j', 'value')


class CellAdmin(admin.ModelAdmin):
    list_display = ('task', 'item', 'criterion', 'value')


class ResultAdmin(admin.ModelAdmin):
    list_display = ('task', 'method', 'item')


admin.site.register(Method, MethodAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Criterion, CriterionAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Cell, CellAdmin)
admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(Param, ParamAdmin)
# admin.site.register(ParamAUX)
admin.site.register(CellDescartesCriterion, CellDescartesCriterionAdmin)
admin.site.register(CellDescartesItem, CellDescartesItemAdmin)

