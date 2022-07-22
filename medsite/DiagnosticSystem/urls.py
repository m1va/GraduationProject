from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('start_consultation/', StartConsultation.as_view(), name='start_consultation'),
    path('vote/', vote, name='vote'),
    path('add_diagnostic/', AddDiagnostic.as_view(), name='add_diagnostic'),
    path('add_employee/', add_employee, name='add_employee'),
    path('add_question/', AddQuestion.as_view(), name='add_question'),
    path('add_disease/', add_disease, name='add_disease'),
    path('add_cabinet/', add_cabinet, name='add_cabinet'),
    path('add_disease-diagnostic/', AddDiseaseDiagnostic.as_view(), name='add_disease-diagnostic'),
    path('set_price_for_diagnostic/', SetPriceForDiagnostic.as_view(), name='set_price_for_diagnostic'),
    path('add_speciality/', AddSpeciality.as_view(), name='add_speciality'),
    path('employees_list/', EmployeesList.as_view(), name='employees_list'),
    path('diagnostic_list/', DiagnosticList.as_view(), name='diagnostic_list'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('consultation_result/', consultation_result, name='consultation_result')
]