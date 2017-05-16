# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Office(models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False)
    name = models.CharField(
        max_length=200,
        null=False,
        verbose_name=_('name'))
    class Meta:
        db_table = 'offices'
        verbose_name = _('Office')
        verbose_name_plural = _('Offices')
        ordering = ['name']
        
    def __unicode__(self):
        return self.name
