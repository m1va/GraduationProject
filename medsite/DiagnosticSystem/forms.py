from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import *


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
            'surname': forms.TextInput(attrs={'class': 'form-input'})
        }

    # Валидатор для примера
    def clean_surname(self):
        surname = self.cleaned_data['surname']
        if len(surname) > 5:
            raise ValidationError('Длина превышает 5 символов')

        return surname


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
