from django import template
from DiagnosticSystem.models import *

register = template.Library()


@register.simple_tag()
def get_patients():
    return Patient.objects.all()
