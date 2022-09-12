# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect
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
#from django.core.urlresolvers import reverse
from django.urls import reverse
from ldap_people.forms import LdapPersonAdminForm
import logging
import sys
from django.conf import settings
from django.utils.html import format_html
from django.contrib import messages
from functools import update_wrapper
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from .forms import AdminChangePasswordForm

class IncorrectLookupParameters(Exception):
    pass

def enable_admin_password_change():
    if hasattr(settings, 'ENABLE_ADMIN_PASSWORD_CHANGE'):
        return settings.ENABLE_ADMIN_PASSWORD_CHANGE
    return False

class LdapPersonAdmin(admin.ModelAdmin):
    form = LdapPersonAdminForm

    search_fields = ['username',]
    readonly_fields = ('full_document','last_login')
    if enable_admin_password_change():
        readonly_fields += ('update_password',)
    fields = ('username','name','surname','email', 'full_document', \
              'alternative_email', 'office','other_office','telephone_number',
              'home_telephone_number', 'floor', 'area', 'position', \
              'host_name','group_id', 'groups_id', 'last_login')
    if enable_admin_password_change():
        fields += ('update_password',)
    actions = None

    
    def full_document(self, obj):
        return "{} {} {}".format( obj.country_document_number,
                                  obj.type_document_number,
                                  obj.document_number )
    full_document.short_description = _('Full_document')

    def last_login(self, obj):
        return obj.info_last_login()
    last_login.short_description = _('Last_login')
    
    def update_password(self, obj):
        if enable_admin_password_change():
            return format_html(
                '<a class="button" href="{}">{}</a>&nbsp;',
                reverse('admin:ldapperson_update_password', args=[obj.username]),
                _('Update_password'),
            )
        else:
            return ''
    update_password.short_description = _('Update_password')

    def get_urls(self):
        

            
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name


        urls = []
        if enable_admin_password_change():
            urls = [
                url(
                    r'^update_password/(?P<id>\w+)/$',
                    self.admin_site.admin_view(self.manage_view),
                    name='ldapperson_update_password',
                ),
            ]
            
        super_urls = super(LdapPersonAdmin, self).get_urls()

        return urls + super_urls



    def manage_view(self, request, id, form_url='', extra_context=None):
        user = None
        opts = LdapPerson._meta

        default_password_lenght = 10
        if hasattr(settings, 'DEFAULT_PASSWORD_LENGHT'):
            default_password_lenght = settings.DEFAULT_PASSWORD_LENGHT
            
        default_password = User.objects.make_random_password(default_password_lenght)
        
        context = {
            'opts':  opts,    
            'change': True,
            'is_popup': False,
            'save_as': False,
            'has_delete_permission': False,
            'has_add_permission': False,
            'has_change_permission': False,
            'default_password': default_password,
        }

        if 'password1' not in request.POST:
            return render(request, 'admin/ldapperson/update_password.html', context)

        params = request.POST.copy()
        form =  AdminChangePasswordForm(params)

        try:
            user = User.objects.get(username=id)
        except Exception as e:
            logging.error(e)
        
        if form.is_valid():
            try:
                new_password = form.cleaned_data['password1']

                logging.warning("updating password for ldap user ...")
                LdapPerson.update_password(id, new_password)

                if not user is None:
                    logging.warning("updating password for django user ...")
                    user.set_password(new_password)
                    user.save()
                
                messages.info(request, _('password_modified_successfully'))
                return HttpResponseRedirect(reverse('admin:ldap_people_ldapperson_change', args=[id]))
            except Exception as e:
                logging.warning(e)
                messages.info(request, e)
                return render(request, 'admin/ldapperson/update_password.html', context)
        else:
            context.update({'form': form})
            messages.info(request, form.errors)
            logging.warning("Invalid confirm change password form, errors: %s" % form.errors)
            return render(request, 'admin/ldapperson/update_password.html', context)


    

    
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
        form = LdapPersonAdminForm(instance=person)

        context = {'form': form,
                   'available_areas': LdapPerson.available_areas(),
                   'available_floors': LdapPerson.available_floors(),
                   'available_employee_types': LdapPerson.available_employee_types(),
                   'available_offices': LdapPerson.available_offices(),
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
        ldap_person= LdapPersonAdminForm(request.POST)
        try:
            if ldap_person.is_valid():
                ldap_person.save()
            else:
                logging.error(ldap_person.errors)

            if 'groups_id' in request.POST:
                new_groups_ids = request.POST.getlist('groups_id')
                LdapGroup.update_member_in_groups(obj.username,new_groups_ids)

            super(LdapPersonAdmin, self).save_model(request, obj, form, change)
            
        except Exception as e:
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
#admin.site.register(AccountAdmin)
