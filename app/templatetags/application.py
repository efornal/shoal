from django import template
from django.conf import settings
import logging


register = template.Library()

@register.filter
def application_title(value):
    title = ''
    if value:
        title = value
    elif settings.APPLICATION_NAME:
        title = settings.APPLICATION_NAME

    return title

@register.filter
def application_subtitle(value):
    subtitle = ''
    if value:
        subtitle = value
    elif settings.APPLICATION_DESC:
        subtitle = settings.APPLICATION_DESC

    return subtitle


@register.filter
def if_not_exist_in(value,objects):
    result = value
    for o in objects:
        if o.name == value:
            result = ''
    return result


@register.filter
def phone_exchange_by_rank_enable(value):
    if (value == 'True') and ( hasattr(settings, 'PHONE_MAPPING') and len(settings.PHONE_MAPPING) > 0 ):
        return True
    elif (value == 'False') and not ( hasattr(settings, 'PHONE_MAPPING') or len(settings.PHONE_MAPPING) > 0 ):
        return True
    else:
        return False


@register.filter
def phone_exchange_by_rank(value):
    result = value
    try:
        prefixs = value.replace('int','').replace(',','/').strip().split("/")
        result = []
        for pre in prefixs:
            if len(pre) > settings.MAX_PHONE_LENGTH:
                result.append([pre,''])
                logging.warning("Incorrect internal number format for: {}".format(pre))
            else:
                match = False
                for n in settings.PHONE_MAPPING:
                    if int(n[0]) <= int(pre) <= int(n[1]):
                        result.append( [pre,"{}".format(n[2])] )
                        match = True
                        break;
                if not match:
                    result.append( [pre,''] )
    except Exception as e:
        logging.error(e)
    return result

@register.filter
def phone_exchange_by_rank_unique(value):
    result = value
    try:
        prefixs = value.replace('int','').replace(',','/').strip().split("/")
        result = []
        for pre in prefixs:
            if len(pre) > settings.MAX_PHONE_LENGTH:
                logging.warning("Internal number omitted, incorrect format for: {}".format(pre))
            else:
                for n in settings.PHONE_MAPPING:
                    if int(n[0]) <= int(pre) <= int(n[1]):
                        result = list(set(result + [n[2]]))
                        break;
    except Exception as e:
        logging.error(e)
    return result
