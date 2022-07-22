from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import *


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class PatientInline(admin.StackedInline):
    model = Patient
    can_delete = False
    verbose_name_plural = 'patient'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (PatientInline,)


# class PatientAdmin(admin.ModelAdmin):
#     list_display = ('id', 'surname', 'name', 'patronymic', 'birthday_date')
#     list_display_links = ('id', 'surname', 'name', 'patronymic')
#     search_fields = ('surname', 'name', 'patronymic')


class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


# admin.site.register(Patient, PatientAdmin)
admin.site.register(Disease, DiseaseAdmin)
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
