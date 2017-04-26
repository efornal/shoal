# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.conf.urls import patterns
from django.http import HttpResponse
from app.models import LdapPerson
from app.models import LdapGroup
from app.models import Office
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
from app.forms import LdapPersonForm

        
class IncorrectLookupParameters(Exception):
    pass


class LdapPersonAdmin(admin.ModelAdmin):
    form = LdapPersonForm
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
        offices = Office.objects.all()
        import logging
        groups = LdapGroup.all()
        groups_of_the_person = [str(x.group_id) for x in LdapGroup.groups_by_uid(person_id)]
        logging.warning(groups_of_the_person)
        context = {'offices': offices,
                   'groups': groups,
                   'groups_of_the_person': groups_of_the_person,
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
        office=''
        
        if 'username' in request.POST and request.POST['username']:
            ldap_username = request.POST['username']
        else:
            logging.error("Attempted to modify the ldap user without having a value.")
            return HttpResponseRedirect('/')
            
        if 'office' in request.POST and request.POST['office']:
            office = request.POST['office']
        elif 'other_office' in request.POST:
            office = request.POST['other_office']

        update_person = { 'username': ldap_username,
                          'telephone_number': request.POST['telephone_number'],
                          'office': office,
                          'email': request.POST['email'],
                          'alternative_email': request.POST['alternative_email'],
                          'floor': request.POST['floor'],
                          'area': request.POST['area'],
                          'position': request.POST['position'],}

        obj.ldap_update(update_person)

        if 'group_id' in request.POST:
            new_groups_ids = request.POST.getlist('group_id')
            LdapGroup.update_member_in_groups(ldap_username,new_groups_ids)

        super(LdapPersonAdmin, self).save_model(request, obj, form, change)

        
        
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
        cl.result_count=len(people)
        
        extra_context={'cl':cl,
                       'result_list':people,
                       'offices': Office.objects.all()}
        return super(LdapPersonAdmin, self).changelist_view( request, extra_context)
        
    change_list_template = "admin/ldapperson/change_list.html"        


admin.site.register(LdapPerson, LdapPersonAdmin)
admin.site.register(Office)
