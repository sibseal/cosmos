import math
from django import forms
from django.core.exceptions import ValidationError
from django.forms import (BaseInlineFormSet, inlineformset_factory)

from .models import *
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['user', 'name']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            # 'user': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        widgets = {
            'name': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'cols': 0, 'placeholder': 'Вариант'}),
        }


class CriteriaForm(forms.ModelForm):
    # content = forms.CharField(widget=forms.Textarea(attrs={"rows": "5"}))
    class Meta:
        model = Criterion
        fields = '__all__'
        widgets = {
            'name': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'cols': 0, 'placeholder': 'Критерий'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'step': "0.01"}),
        }


class CriterionFormSetCustom(BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return
        sum = 0
        for form in self.forms:
            name = form.cleaned_data.get('name')
            value = form.cleaned_data.get('value')
            print('>>', name, value)
            if value:
                sum += value
        print(sum, len(self.forms))
        if len(self.forms) != 0 and not math.isclose(sum, 1):
            raise ValidationError("Сумма вероятностей наступления должна быть равна 1!")


CriterionFormSet = inlineformset_factory(
    Task,
    Criterion,
    form=CriteriaForm,
    extra=0,
    can_delete=False,
    can_delete_extra=True,
    formset=CriterionFormSetCustom
)

ItemFormSet = inlineformset_factory(
    Task,
    Item,
    form=ItemForm,
    extra=0,
    can_delete=False,
    can_delete_extra=True
)


class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)
