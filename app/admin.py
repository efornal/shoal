# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.conf.urls import patterns
from django.http import HttpResponse
from ldap_people.models import LdapPerson
from ldap_people.models import LdapGroup
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
from ldap_people.forms import LdapPersonForm
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

admin.site.register(Office)
