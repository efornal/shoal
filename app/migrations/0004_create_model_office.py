# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-07 10:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_change_meta_options_on_ldapperson'),
    ]

    operations = [
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, verbose_name='nombre')),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'offices',
                'verbose_name': 'Oficina',
                'verbose_name_plural': 'Offices',
            },
        ),
        migrations.AlterModelOptions(
            name='ldapperson',
            options={'managed': False, 'verbose_name': 'LdapPerson', 'verbose_name_plural': 'LdapPeople'},
        ),
    ]
