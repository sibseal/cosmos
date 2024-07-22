from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField

class Param(models.Model):
    name = models.CharField(max_length=8)
    description = models.CharField(max_length=64, blank=True)
    single = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - {self.description}'

class Method(models.Model):
    name = models.CharField(max_length=64)
    name_short = models.CharField(max_length=16)
    need_criterion_weight = models.BooleanField(default=False)
    control_sum_of_criteria = models.BooleanField(default=False)
    need_criterion_direction = models.BooleanField(default=False)
    need_descartes_criterion = models.BooleanField(default=False)
    need_descartes_item = models.BooleanField(default=False)
    params = models.ManyToManyField(Param, blank=True)
    image = models.ImageField(upload_to='images', blank=True)
    content = RichTextField(blank=True)

    def __str__(self):
        return self.name_short


class Task(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.PROTECT)
    name = models.CharField(max_length=150)
    result = models.JSONField(default=dict, blank=True)
    methods = models.ManyToManyField(Method)
    aux_params = models.JSONField(default=dict, blank=True)
    changed = models.BooleanField(default=False)
    enable_normalization = models.BooleanField(default=False)
    use_normalized = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class Item(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    name_short = models.CharField(max_length=5, blank=False)

    def __str__(self):
        return self.name


class Criterion(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    name_short = models.CharField(max_length=5, blank=False)
    value = models.FloatField()
    direction_bool = models.BooleanField(default=False)
    changed = models.BooleanField(default=False)
    normalize_param_p = models.FloatField(default=0)
    normalize_param_k = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Cell(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    value = models.FloatField()
    value_normalized = models.FloatField()
    changed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.task.name}_{self.item.name}_{self.criterion.name}'


class CellDescartesCriterion(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    type = models.CharField(max_length=64)
    id_i = models.IntegerField()
    id_j = models.IntegerField()
    value = models.FloatField(default=0)
    changed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}_{self.task.name}_{self.id_i}_{self.id_j}'


class CellDescartesItem(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    id_i = models.IntegerField()
    id_j = models.IntegerField()
    value = models.FloatField(default=0)
    changed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}_{self.task.name}_{self.id_i}_{self.id_j}'


class ParamAUX(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    param = models.ForeignKey(Param, on_delete=models.CASCADE, blank=True, null=True)
    value = models.FloatField(blank=True)
    changed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.task.name}_{self.param.name}'


class Question(models.Model):
    step = models.IntegerField(blank=True, null=True)
    question_text = models.CharField(max_length=200)
    description = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f'{self.question_text}'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    next_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='next_question', blank=True, null=True)
    choice_text = models.CharField(max_length=200)
    methods = models.ManyToManyField(Method, blank=True)

    def __str__(self):
        return self.choice_text


class Result(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='result_task')
    method = models.ForeignKey(Method, on_delete=models.CASCADE, related_name='result_method')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='result_item')


class Setting(models.Model):
    max_items = models.IntegerField(default=4)
    max_criterions = models.IntegerField(default=4)
