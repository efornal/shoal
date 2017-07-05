# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-05 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ldap_people', '0005_rename_ldapperson_to_ldap_people_ldapperson'),
    ]

    operations = [
        migrations.RunSQL("ALTER TABLE ldap_people_ldapperson ADD COLUMN host_name varchar(200);",
                      "ALTER TABLE ldap_people_ldapperson DROP COLUMN host_name;"),
    ]
