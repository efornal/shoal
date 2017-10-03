# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.http import HttpResponse
from ldap_people.models import LdapPerson
from ldap_people.models import LdapOffice
from ldap_people.models import LdapGroup
from ldap_people.models import Office
from django.forms import ModelForm
from django import forms
from django.conf.urls import url
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db.models.query import QuerySet
from django.contrib.admin.views.main import ChangeList
from django.db import models
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from ldap_people.forms import LdapPersonForm
import logging
import sys
from django.conf import settings


class IncorrectLookupParameters(Exception):
    pass



class LdapPersonAdminForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        max_length=200)
    name = forms.CharField(
        max_length=200,
        required=True,
        label=_('name'))
    surname = forms.CharField(
        max_length=200,
        required=True)
    fullname = forms.CharField(
        max_length=200,
        required=False)
    email = forms.EmailField(
        max_length=200,
        required=True)
    alternative_email = forms.EmailField(
        max_length=200,
        required=False)
    office = forms.ChoiceField(
        choices=[(office.name, office.name) for office in LdapOffice.all()],
        required=True,
        label=_('office'))
    other_office = forms.CharField(
        max_length=200,
        required=False,
        label=_('other_office'))
    group_id = forms.ChoiceField(
        choices=[(group.name, group.name) for group in LdapGroup.all()],
        required=False,
        label=_('gooup'))
    groups_id = forms.MultipleChoiceField(
        widget=forms.SelectMultiple,
        choices=[(group.name, group.name) for group in LdapGroup.all()],
        required=False,
        label=_('gooup'))

    # group_id = forms.CharField(
    #     max_length=200,
    #     required=False)
    document_number = forms.CharField(
        max_length=200,
        required=False)
    type_document_number = forms.CharField(
        max_length=200,
        required=False)
    telephone_number = forms.CharField(
        max_length=200,
        required=False)
    home_telephone_number = forms.CharField(
        max_length=200,
        required=False)
    floor = forms.CharField(
        max_length=200,
        required=False)
    area = forms.CharField(
        max_length=200,
        required=False)
    position = forms.CharField(
        max_length=200,
        required=False)
    host_name = forms.CharField(
        max_length=200,
        required=False)

    class Meta:
        model = LdapPerson
        fields = ('username','name','surname','email','alternative_email',
                  'document_number','type_document_number', 'host_name', \
                  'office','telephone_number','home_telephone_number','other_office')




class LdapPersonAdmin(admin.ModelAdmin):
    form = LdapPersonAdminForm
    readonly_fields = ('username',)
    search_fields = ['username',]
    list_display = ('username','name','surname','email','document_number', \
                    'office','telephone_number','other_office')
    actions = None


    def get_object(self, request, object_id, from_field=None):
        """
        Returns an instance matching the field and value provided, the primary
        key is used if no field is provided. Returns ``None`` if no match is
        found or the object_id fails validation.
        """
        queryset = self.get_queryset(request)
        person = LdapPerson.get_by_uid('{}'.format(object_id))
        model =  person
        return person

    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        person_id = '{}'.format(object_id)
        person = LdapPerson.get_by_uid(person_id)
        form = LdapPersonForm(instance=person)
        groups = LdapGroup.all()
        groups_of_the_person = [str(x.group_id) for x in LdapGroup.groups_by_uid(person_id)]

        context = {'form': form,
                   'groups': groups,
                   'groups_of_the_person': groups_of_the_person,
                   'available_areas': LdapPerson.available_areas(),
                   'available_floors': LdapPerson.available_floors(),
                   'available_employee_types': LdapPerson.available_employee_types(),
                   'result': person,}

        if extra_context is None:
            extra_context = context
        else:
            extra_context.update(context)

        return super(LdapPersonAdmin, self).change_view(
            request, object_id, form_url, extra_context
        )
    change_form_template = "admin/ldapperson/change_form.html"

    
    def save_model(self, request, obj, form, change):
        ldap_person= LdapPersonForm(request.POST)
        try:
            if ldap_person.is_valid():
                ldap_person.save()
            else:
                logging.error(ldap_person.errors)

            if 'groups_id' in request.POST:
                new_groups_ids = request.POST.getlist('groups_id')
                LdapGroup.update_member_in_groups(obj.username,new_groups_ids)

            super(LdapPersonAdmin, self).save_model(request, obj, form, change)
            
        except Exception, e:
            for msg in e:
                messages.warning(request, msg)
        
        
    def changelist_view(self, request, extra_context=""):
        if 'q' in request.GET:
            people = LdapPerson.search('{}'.format(request.GET['q']))
        else:
            people = []
            
        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)
        list_filter = self.get_list_filter(request)
        search_fields = self.get_search_fields(request)
        
        list_select_related = self.get_list_select_related(request)

        opts = self.model._meta

        ChangeList = self.get_changelist(request)
        try:
            cl = ChangeList(
                request, self.model, list_display,
                list_display_links, list_filter, self.date_hierarchy,
                search_fields, list_select_related, self.list_per_page,
                self.list_max_show_all, self.list_editable, self,
            )
        except IncorrectLookupParameters:
            if ERROR_FLAG in request.GET.keys():
                return SimpleTemplateResponse('admin/invalid_setup.html', {
                    'title': _('Database error'),
                })
            return HttpResponseRedirect(request.path + '?' + ERROR_FLAG + '=1')


        cl.result_list=people
        if people is None:
            messages.warning(request, _('search_error'))
            cl.result_count=0
        else:
            cl.result_count=len(people)
        
        extra_context={'cl':cl,
                       'result_list':people,}
        return super(LdapPersonAdmin, self).changelist_view( request, extra_context)
        
    change_list_template = "admin/ldapperson/change_list.html"        


class OfficeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ('name',)
    
admin.site.register(LdapPerson, LdapPersonAdmin)
admin.site.register(Office, OfficeAdmin)
