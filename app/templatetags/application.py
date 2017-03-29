from django import template
from django.conf import settings


register = template.Library()


@register.filter
def application_title(value):
    title = ''
    if value:
        title = value
    elif settings.APPLICATION_NAME:
        title = settings.APPLICATION_NAME

    return title
