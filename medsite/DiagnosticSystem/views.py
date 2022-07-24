from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.utils import timezone

from django.db.models import Sum

from .models import Questions, Answers, PatientAnswers

from .forms import *
from .models import *

sidebar = [{'title': "Начать консультацию", 'url_name': 'start_consultation'},
           {'title': "Добавить врача", 'url_name': 'add_employee'},
           {'title': "Добавить диагностику", 'url_name': 'add_diagnostic'},
           {'title': "Добавить вопрос для диагностики", 'url_name': 'add_question'},
           {'title': "Добавить кабинет", 'url_name': 'add_cabinet'},
           {'title': "Добавить специальность", 'url_name': 'add_speciality'},
           {'title': "Связать заболевание с диагностикой", 'url_name': 'add_disease-diagnostic'},
           {'title': "Установить цену на диагностику", 'url_name': 'set_price_for_diagnostic'},
           {'title': "Просмотреть список врачей", 'url_name': 'employees_list'},
           {'title': "Просмотреть список диагностик", 'url_name': 'diagnostic_list'},
           {'title': "Добавление функций принадлежности", 'url_name': 'add_membership_chart'}
           ]
menu = [{'title': "Главная страница", 'url_name': 'home'},
        {'title': "Диагностика", 'url_name': 'home'}
        ]


def function(x, a, b, c, d):
    if x == a == b or x == c == d:
        coef = 1
        return coef
    elif x <= a:
        coef = 0
        return coef
    elif a <= x < b:
        coef = x - a / b - a
        return coef
    elif b <= x < c:
        coef = 1
        return coef
    elif c <= x < d:
        coef = d - x / d - c
        return coef
    elif d <= x:
        coef = 0
        return coef


def coef_convert_to_user_friendly(coef_list):
    if coef_list[0] > coef_list[1]:
        return "Низкая вероятность"
    elif coef_list[1] > coef_list[2]:
        return "Средняя вероятность"
    else:
        return "Высокая вероятность"


# def result(request):
#     context = {
#         'menu': menu,
#         'title': 'Диагностика',
#         'sidebar': sidebar
#     }
#
#     if request.method == 'POST':
#
#
#     return render(request, 'DiagnosticSystem/index.html', context=context)


def index(request):
    Employees = Patient.objects.all()
    context = {
        'menu': menu,
        'employees': Employees,
        'title': 'Диагностика',
        'sidebar': sidebar
    }

    return render(request, 'DiagnosticSystem/index.html', context=context)


def vote(request):
    patient = Patient.objects.get(pk=request.user.id)
    questions = Questions.objects.all()
    selected_answers = []
    try:
        for question in questions:
            selected_answers.append(question.answers_set.get(pk=request.POST['answer_for_question' + str(question.id)]))
        time_selected = timezone.now()
    except (KeyError, Answers.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'DiagnosticSystem/start_consultation.html', {
            'menu': menu,
            'sidebar': sidebar,
            'title': 'Диагностика',
            'questions': questions,
            'error_message': "You didn't select a choice."
        })
    else:
        for answer in selected_answers:
            PatientAnswers.objects.create(answer=answer, patient=patient, question=answer.question,
                                          answer_date=time_selected)
        """ Подсчет коэффициентов """
        points_for_disease = PatientAnswers.objects.select_related('answer', 'answer__disease') \
            .values_list('answer__disease__id', 'answer__disease__name', 'answer__disease__membership_chart_id') \
            .annotate(total=Sum('answer__number_of_points')) \
            .filter(patient=patient, answer_date=time_selected)
        # print(points_for_disease.query)
        print(points_for_disease)
        possible_diseases_list = []
        for p in points_for_disease:
            membership_functions = MembershipFunction.objects.values_list('function_name', 'a', 'b', 'c', 'd') \
                .filter(membership_chart=p[2])  # p[2] == membership_chart_id
            coef_list = []
            for m_f in membership_functions:
                coef = function(p[3], m_f[1], m_f[2], m_f[3], m_f[4])
                coef_list.append(coef)
                # print('p[3]', p[3], 'm_f[1]', m_f[1], 'm_f[2]', m_f[2], 'm_f[3]', m_f[3], 'm_f[4]', m_f[4])
            print(coef_list)
            probability = coef_convert_to_user_friendly(coef_list)
            possible_disease = {'disease_name': p[1], 'probability': probability}
            possible_diseases_list.append(possible_disease)

            print(possible_diseases_list)
            # print(membership_functions)
            # print(membership_functions[0])

            # print(p.patient.id, p.answer.title, p.answer.disease.name, p.answer.number_of_points)
        return render(request, 'DiagnosticSystem/consultation_result.html',
                      {'possible_diseases_list': possible_diseases_list})


class StartConsultation(CreateView):
    form_class = PatientAnswersForm
    template_name = 'DiagnosticSystem/start_consultation.html'
    success_url = reverse_lazy('vote')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['sidebar'] = sidebar
        context['title'] = 'Диагностика'
        context['questions'] = self.get_queryset()
        return context

    def get_queryset(self):
        return Questions.objects.all()


# class StartConsultation(CreateView):
#     form_class = PatientAnswersForm
#     template_name = 'DiagnosticSystem/start_consultation.html'
#     success_url = reverse_lazy('start_consultation')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['menu'] = menu
#         context['sidebar'] = sidebar
#         context['title'] = 'Диагностика'
#         context['questions'] = self.get_queryset()
#         return context
#
#     def get_queryset(self):
#         return Questions.objects.all()


class AddDiagnostic(CreateView):
    form_class = AddDiagnosticForm
    template_name = 'DiagnosticSystem/add_diagnostic.html'
    success_url = reverse_lazy('add_diagnostic')
    success_message = "Диагностика добавлена!"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['sidebar'] = sidebar
        context['title'] = 'Добавление диагностики'
        return context


# def add_diagnostic(request):
#     if request.method == 'POST':
#         form = AddDiagnosticForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             form.save()
#             return redirect('add_diagnostic')
#     else:
#         form = AddDiagnosticForm()
#
#     return render(request, 'DiagnosticSystem/add_diagnostic.html',
#                   {'form': form, 'title': 'Добавление диагностики', 'sidebar': sidebar})

class AddDiseaseDiagnostic(CreateView):
    form_class = AddDiseaseDiagnosticForm
    template_name = 'DiagnosticSystem/add_disease-diagnostic.html'
    success_url = reverse_lazy('add_disease-diagnostic')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
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
                  {'menu': menu, 'form': form, 'title': 'Добавление врача', 'sidebar': sidebar})


# def add_question(request):
#     if request.method == 'POST':
#         form = AddQuestionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('add_question')
#     else:
#         form = AddQuestionForm()
#
#     return render(request, 'DiagnosticSystem/add_question.html',
#                   {'form': form, 'title': 'Добавление вопроса', 'sidebar': sidebar})


class AddQuestion(CreateView):
    form_class = AddQuestionForm
    template_name = 'DiagnosticSystem/add_question.html'
    success_url = reverse_lazy('add_question')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['sidebar'] = sidebar
        context['title'] = 'Добавление вопроса'
        return context


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
        context['menu'] = menu
        context['sidebar'] = sidebar
        context['title'] = 'Добавление специальности'
        return context


class SetPriceForDiagnostic(CreateView):
    form_class = SetPriceForDiagnosticForm
    template_name = 'DiagnosticSystem/set_price_for_diagnostic.html'
    success_url = reverse_lazy('set_price_for_diagnostic.html')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['sidebar'] = sidebar
        context['title'] = 'Установить цену на диагностику'
        return context


class EmployeesList(ListView):
    model = Employee
    template_name = 'DiagnosticSystem/employees_list.html'
    context_object_name = 'employees'

    # extra_context = {'title': 'Список сотрудников'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['sidebar'] = sidebar
        context['title'] = 'Список сотрудников'
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
        context['menu'] = menu
        context['sidebar'] = sidebar
        context['title'] = 'Добавление диагностики'
        return context


# def diagnostic_list(request):
#     Diagnostics = Diagnostic.objects.all()
#
#     return render(request, 'DiagnosticSystem/diagnostic_list.html',
#                   {'diagnostics': Diagnostics, 'title': 'Список диагностик', 'sidebar': sidebar})


class AddMembershipChart(CreateView):
    form_class = AddMembershipFunctionForm
    template_name = 'DiagnosticSystem/add_membership_chart.html'
    success_url = reverse_lazy('add_membership_chart')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Добавление функций принадлежности'
        context['sidebar'] = sidebar
        return context


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'DiagnosticSystem/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'DiagnosticSystem/login.html'

    # success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


def consultation_result(request):
    context = {
        'menu': menu,
        'title': 'Результат диагностики',
        'sidebar': sidebar,
    }

    return render(request, 'DiagnosticSystem/consultation_result.html', context=context)
