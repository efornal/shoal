# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings

from django.shortcuts import redirect

def enable_user_password_change(view):
    def wrap(request, *args, **kwargs):
        if hasattr(settings, 'ENABLE_USER_PASSWORD_CHANGE') \
           and settings.ENABLE_USER_PASSWORD_CHANGE:
            return view(request, *args, **kwargs)
        else:
            return redirect('index')
    return wrap
