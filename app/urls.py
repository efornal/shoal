# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': settings.LOGIN_REDIRECT_URL},
        name='logout'),
    url(r'^search',views.search, name='search'),
    url(r'^edit/$',views.edit, name='edit'),
    url(r'^save/$',views.save, name='save'),
    url(r'^en/$', views.index, name='index'),
    url(r'^lang/(?P<lang>\w+)/$', views.set_language, name='set_language'),
    url(r'^$', views.index, name='index'),
]
