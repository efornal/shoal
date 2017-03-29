from django import template
from django.conf import settings


register = template.Library()

import logging
@register.filter
def application_title(value):
    logging.error(settings.APPLICATION_NAME)
    title = ''
    if value:
        title = value
    elif settings.APPLICATION_NAME:
        title = settings.APPLICATION_NAME

    return title
