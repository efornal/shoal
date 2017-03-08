from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from .models import LdapConn
from django.shortcuts import redirect
from django.utils import translation
import logging


def index(request):
    context={}
    people = LdapConn.people_by_uid('ef')
    context.update({'people': people})
    return render(request, 'index.html', context)


def search(request):
    context={}

    return render(request, 'index.html', context)
