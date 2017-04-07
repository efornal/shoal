# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.conf.urls import patterns
from django.http import HttpResponse
from app.models import LdapPerson
from app.models import Office
from django.forms import ModelForm
from django import forms
from django.conf.urls import url
import logging
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
    fields = ('username','name','surname','email','document_number', \
              'office','telephone_number')
    form = LdapPersonForm
    readonly_fields = ('username',)
    search_fields = ['username',]
    actions = None


    def get_object(self, request, object_id, from_field=None):
        """
        Returns an instance matching the field and value provided, the primary
        key is used if no field is provided. Returns ``None`` if no match is
        found or the object_id fails validation.
        """
        queryset = self.get_queryset(request)
        people = LdapPerson.get_by_uid('{}'.format(object_id))
        model =  people
        return people

    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.method == 'GET':
            people = LdapPerson.get_by_uid('{}'.format(object_id))
            extra_context={'result': people}

        extra_context.update({'offices': Office.objects.all()})
        return super(LdapPersonAdmin, self).change_view(
            request, object_id, form_url, extra_context
        )
    change_form_template = "admin/ldapperson/change_form.html"

    
    def save_model(self, request, obj, form, change):
        person = { 'username': request.POST['username'],
                   'telephone_number': request.POST['telephone_number'],
                   'office': request.POST['office'],
        }

        if 'username' in request.POST and request.POST['username']:
            obj.ldap_update(person)
            super(LdapPersonAdmin, self).save_model(request, obj, form, change)
        else:
            return HttpResponseRedirect('/')

        
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
