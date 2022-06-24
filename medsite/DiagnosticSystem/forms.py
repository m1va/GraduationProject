from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import *
from django.contrib import messages

import re

regex = "^[а-яА-ЯёЁ-]+$"


class AddDiagnosticForm(forms.ModelForm):
    # name = forms.CharField(max_length=50, label="Название")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Diagnostic
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'})
        }

    # Валидатор диагностики
    def clean_name(self):
        diagnostic = self.cleaned_data['name']
        if len(diagnostic) > 64:
            raise ValidationError('Ошибка. Длина превышает 64 символа!')
        elif len(diagnostic) < 3:
            raise ValidationError('Ошибка. Длина меньше 3-х символов!')
        elif any(map(str.isdigit, diagnostic)):
            raise ValidationError('Ошибка. Присутствуют цифры!')
        elif not re.match(regex, diagnostic):
            raise ValidationError('Ошибка. Недопустимые символы!')

        return diagnostic


class AddDiseaseDiagnosticForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['disease'].empty_label = "Заболевание не выбрано"
        self.fields['diagnostic'].empty_label = "Диагностика не выбрана"

    class Meta:
        model = DiseaseDiagnostics
        fields = '__all__'


class AddEmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cabinet'].empty_label = "Кабинет не выбран"
        self.fields['speciality'].empty_label = "Специальность не выбрана"

    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'surname': forms.TextInput(attrs={'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-input'})
        }

    # # Валидатор для примера
    # def clean_surname(self):
    #     surname = self.cleaned_data['surname']
    #     if len(surname) > 5:
    #         raise ValidationError('Длина превышает 5 символов')
    #
    #     return surname


# class AddEmployeeForm(forms.Form):
#     surname = forms.CharField(max_length=50, label="Фамилия")
#     name = forms.CharField(max_length=50, label="Имя")
#     patronymic = forms.CharField(max_length=50, label="Отчество")
#     birthday_date = forms.DateField(label="Дата рождения")

# 59строка


class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = '__all__'
    #  widgets = {
    #      'name': forms.TextInput(attrs={'class': 'form-input'})
    #  }


class AddDiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = '__all__'


class AddCabinetForm(forms.ModelForm):
    class Meta:
        model = Cabinet
        fields = '__all__'


class AddSpecialityForm(forms.ModelForm):
    class Meta:
        model = Speciality
        fields = '__all__'


class SetPriceForDiagnosticForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = '__all__'


class PatientAnswersForm(forms.ModelForm):
    class Meta:
        model = PatientAnswers
        fields = '__all__'


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form_input'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form_input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form_input'}))
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form_input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.TextInput(attrs={'class': 'form_input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.TextInput(attrs={'class': 'form_input'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form_input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form_input'}))

