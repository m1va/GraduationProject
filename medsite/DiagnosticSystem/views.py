from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import *
from .models import *

sidebar = [{'title': "Добавить врача", 'url_name': 'add_employee'},
           {'title': "Добавить диагностику", 'url_name': 'add_diagnostic'},
           {'title': "Добавить вопрос для диагностики", 'url_name': 'add_question'},
           {'title': "Добавить кабинет", 'url_name': 'add_cabinet'},
           {'title': "Добавить специальность", 'url_name': 'add_speciality'},
           {'title': "Связать заболевание с диагностикой", 'url_name': 'add_disease-diagnostic'},
           {'title': "Установить цену на диагностику", 'url_name': 'set_price_for_diagnostic'},
           {'title': "Просмотреть список врачей", 'url_name': 'employees_list'},
           {'title': "Просмотреть список диагностик", 'url_name': 'diagnostic_list'}
           ]
menu = ['Главная страница', 'Диагностика', 'Войти']


def index(request):
    Employees = Patient.objects.all()
    context = {
        'menu': menu,
        'employees': Employees,
        'title': 'Диагностика',
        'sidebar': sidebar
    }

    return render(request, 'DiagnosticSystem/index.html', context=context)


class AddDiagnostic(CreateView):
    form_class = AddDiagnosticForm
    template_name = 'DiagnosticSystem/add_diagnostic.html'
    success_url = reverse_lazy('add_diagnostic')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = sidebar
        context['title'] = 'Добавление диагностики'
        return context


class AddDiseaseDiagnostic(CreateView):
    form_class = AddDiseaseDiagnosticForm
    template_name = 'DiagnosticSystem/add_disease-diagnostic.html'
    success_url = reverse_lazy('add_disease-diagnostic')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = sidebar
        context['title'] = 'Связать заболевание с диагностикой'
        return context


def add_employee(request):
    if request.method == 'POST':
        form = AddEmployeeForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            return redirect('add_employee')
    else:
        form = AddEmployeeForm()

    return render(request, 'DiagnosticSystem/add_employee.html',
                  {'form': form, 'title': 'Добавление врача', 'sidebar': sidebar})


def add_question(request):
    if request.method == 'POST':
        form = AddQuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_question')
    else:
        form = AddQuestionForm()

    return render(request, 'DiagnosticSystem/add_question.html',
                  {'form': form, 'title': 'Добавление вопроса', 'sidebar': sidebar})


def add_disease(request):
    if request.method == 'POST':
        form = AddDiseaseForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            return redirect('add_disease')
    else:
        form = AddDiseaseForm()

    return render(request, 'DiagnosticSystem/add_disease.html',
                  {'form': form, 'title': 'Добавление заболевания', 'sidebar': sidebar})


def add_cabinet(request):
    if request.method == 'POST':
        form = AddCabinetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_cabinet')
    else:
        form = AddCabinetForm()

    return render(request, 'DiagnosticSystem/add_cabinet.html',
                  {'form': form, 'title': 'Добавление кабинета', 'sidebar': sidebar})


class AddSpeciality(CreateView):
    form_class = AddSpecialityForm
    template_name = 'DiagnosticSystem/add_speciality.html'
    success_url = reverse_lazy('add_speciality')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = sidebar
        context['title'] = 'Добавление специальности'
        return context


class SetPriceForDiagnostic(CreateView):
    form_class = SetPriceForDiagnosticForm
    template_name = 'DiagnosticSystem/set_price_for_diagnostic.html'
    success_url = reverse_lazy('set_price_for_diagnostic.html')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = sidebar
        context['title'] = 'Установить цену на диагностику'
        return context


class EmployeesList(ListView):
    model = Patient
    template_name = 'DiagnosticSystem/employees_list.html'
    context_object_name = 'employees'
    extra_context = {'title': 'Список сотрудников'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = sidebar
        context['title'] = 'Добавление сотрудника'
        return context


# def employees_list(request):
#     Employees = Patient.objects.all()
#
#     return render(request, 'DiagnosticSystem/employees_list.html',
#                   {'employees': Employees, 'title': 'Список сотрудников', 'sidebar': sidebar})


class DiagnosticList(ListView):
    model = Diagnostic
    template_name = 'DiagnosticSystem/diagnostic_list.html'
    context_object_name = 'diagnostics'
    extra_context = {'title': 'Список диагностик'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = sidebar
        context['title'] = 'Добавление диагностики'
        return context

# def diagnostic_list(request):
#     Diagnostics = Diagnostic.objects.all()
#
#     return render(request, 'DiagnosticSystem/diagnostic_list.html',
#                   {'diagnostics': Diagnostics, 'title': 'Список диагностик', 'sidebar': sidebar})