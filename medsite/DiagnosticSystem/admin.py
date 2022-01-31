from django.contrib import admin

from .models import *


class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'surname', 'name', 'patronymic', 'birthday_date')
    list_display_links = ('id', 'surname', 'name', 'patronymic')
    search_fields = ('surname', 'name', 'patronymic')


class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Patient, PatientAdmin)
admin.site.register(Disease, DiseaseAdmin)
