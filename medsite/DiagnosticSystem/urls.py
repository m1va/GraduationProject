from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('add_diagnostic/', AddDiagnostic.as_view(), name='add_diagnostic'),
    path('add_employee/', add_employee, name='add_employee'),
    path('add_question/', add_question, name='add_question'),
    path('add_disease/', add_disease, name='add_disease'),
    path('add_cabinet/', add_cabinet, name='add_cabinet'),
    path('add_disease-diagnostic/', AddDiseaseDiagnostic.as_view(), name='add_disease-diagnostic'),
    path('set_price_for_diagnostic/', SetPriceForDiagnostic.as_view(), name='set_price_for_diagnostic'),
    path('add_speciality/', AddSpeciality.as_view(), name='add_speciality'),
    path('employees_list/', EmployeesList.as_view(), name='employees_list'),
    path('diagnostic_list/', DiagnosticList.as_view(), name='diagnostic_list')
]