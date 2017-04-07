# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.forms import ModelForm
from .models import LdapPerson
from .models import Office
from django.utils.translation import ugettext as _
from django.utils import translation
from django.contrib import messages
import logging
from django.conf import settings


class LdapPersonForm(forms.ModelForm):
    username = forms.CharField(
        max_length=200)
    name = forms.CharField(
        max_length=200,
        required=False,
        label=_('name'))
    person_id = forms.CharField(
        max_length=200,
        required=False)
    surname = forms.CharField(
        max_length=200,
        required=False)
    fullname = forms.CharField(
        max_length=200,
        required=False)
    email = forms.CharField(
        max_length=200,
        required=False)
    office = forms.CharField(
        max_length=200,
        required=False,
        label=_('office'))
    other_office = forms.CharField(
        max_length=200,
        required=False,
        label=_('other_office'))
    group_id = forms.CharField(
        max_length=200,
        required=False)
    document_number = forms.CharField(
        max_length=200,
        required=False)
    telephone_number = forms.CharField(
        max_length=200,
        required=False)

    class Meta:
        model = LdapPerson
        fields = ('username','name','surname','email','document_number', \
                  'office','telephone_number','other_office')

# class LdapPerson(models.Model):
#     username = models.CharField(max_length=200)
#     document = models.CharField(max_length=200) 
#     name = models.CharField(max_length=200)
#     surname = models.CharField(max_length=200)
#     email = models.CharField(max_length=200)
#     office   = forms.ModelChoiceField(
#         queryset=Office.objects.all(),
#         empty_label= "(%s)" % _('specify_other'),
#         to_field_name= "id",
#         required=False,
#         label=_('office'))
#     telephone_number = models.CharField(max_length=200)


#     class Meta:
#         model = LdapPerson
#         fields = ('username',
#                   'name',
#                   'surname',
#                   'document',
#                   'office',
#                   'telephone_number',
#                   'other_office',)
