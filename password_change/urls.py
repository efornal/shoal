# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import auth
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^accounts/password/change/$',
        auth.password_change, name='auth_password_change'),
    url(r'^accounts/password/change/complete/$',
        auth.password_change_complete, name='auth_password_change_complete'),
]
