# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import auth
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^accounts/password/reset/$',
        auth.password_reset, name='auth_password_reset'),
    url(r'^accounts/password/reset/complete/$',
        auth.password_reset_complete, name='auth_password_reset_complete'),
    url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth.password_reset_confirm, name='auth_password_reset_confirm'),
    url(r'^accounts/password/change/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth.password_change, name='auth_password_change'),
]
