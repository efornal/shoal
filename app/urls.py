# -*- coding: utf-8 -*-
from django.urls import path, re_path
#from __future__ import unicode_literals
from django.conf.urls import include
#from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from password_change import urls as change_password_urls
from django.views.generic import RedirectView

urlpatterns = [
    path('', include(change_password_urls)),
    re_path('api/user/(?P<user>\w+)/host/(?P<host>(\w+)?.\w+)/register', \
        views.api_register_host, name='api_register_host'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(),{'next_page': 'logout_message'},name='logout'),
    path('logout/message',views.logout_message, name='logout_message'),
    re_path('search/office/(?P<office>.*)/',
        views.search_by_office, name='search_by_office'),
    path('search/',views.search, name='search'),
    path('edit/',views.edit, name='edit'),
    path('save/',views.save, name='save'),
    path('en/', views.index, name='index'),
    re_path('lang/(?P<lang>\w+)/', views.set_language, name='set_language'),
    path('favicon\.ico',RedirectView.as_view(url='/static/images/favicon.ico')),
    path('', views.index, name='index'),
]

