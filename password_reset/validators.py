import logging
from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings
import dns.resolver, dns.exception

def validate_email_domain_to_exclude(value):
    logging.info('Checking email domain in preset domains..')
    invalid_domains = []
    try:
        email_domain = value.split('@')[1]
        invalid_domains = settings.VALIDATE_EMAIL_DOMAINS_TO_EXCLUDE
    except AttributeError, e:
        logging.warning("Email domain verification is omitted. %s", e)
    except Exception, e:
        logging.warning("Email domain verification failed. %s", e)
        raise forms.ValidationError(_('email_domain_not_exist'))
    
    if email_domain in invalid_domains:
        logging.warning("Invalid email domain {}, restricted are {}"
                        .format(email_domain, invalid_domains))
        raise forms.ValidationError(_('email_domain_to_exclude'))
    return value

def validate_email_domain_restriction(value):
    logging.info('Checking email domain in preset domains..')
    valid_domains = []
    try:
        email_domain = value.split('@')[1]
        valid_domains = settings.VALIDATE_EMAIL_DOMAINS
    except AttributeError, e:
        logging.warning("Email domain verification is omitted. %s", e)
    except Exception, e:
        logging.warning("Email domain verification failed. %s", e)
        raise forms.ValidationError(_('email_domain_not_exist'))
    
    if email_domain not in valid_domains:
        logging.warning("Invalid email domain {}, valid are {}"
                        .format(email_domain, valid_domains))
        raise forms.ValidationError(_('email_domain_restriction'))
    return value


def validate_existence_email_domain(value):
    logging.info('Checking the existence of the email domain..')
    validate = False
    try:
        validate = settings.VALIDATE_EXISTENCE_EMAIL_DOMAIN
    except AttributeError, e:
        logging.warning("Email domain existence is omitted. %s", e)
        return value
    
    try:
        if validate:
            email_domain = value.split('@')[1]
            results = dns.resolver.query(email_domain, 'MX')
    except dns.exception.DNSException, e:
        logging.warning('Domain does not exist. %s', e)
        raise forms.ValidationError(_('email_domain_not_exist'))
    except Exception, e:
        logging.error('ERROR Exception: %s',e)

    return value

