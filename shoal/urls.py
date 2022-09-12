# -*- coding: utf-8 -*-
#rom __future__ import unicode_literals
from django.urls import include, path
from django.contrib import admin
#from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
#dmin.autodiscover()

urlpatterns = [
    path('internos/', include('app.urls')),
    path('admin/', admin.site.urls ),
]
#urlpatterns += i18n_patterns(
#    path('', include('app.urls')),
#)


