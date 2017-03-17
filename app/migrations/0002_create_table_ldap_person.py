# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-17 16:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_create_model_ldap_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='LdapPerson',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=200)),
                ('person_id', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('surname', models.CharField(max_length=200)),
                ('fullname', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('office', models.CharField(max_length=200)),
                ('group_id', models.CharField(max_length=200)),
                ('document_number', models.CharField(max_length=200)),
                ('type_document_number', models.CharField(max_length=200)),
                ('country_document_number', models.CharField(max_length=200)),
                ('telephone_number', models.CharField(max_length=200)),
                ('home_telephone_number', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'app_ldapperson',
                'verbose_name': 'LdapPerson',
                'verbose_name_plural': 'LdapPeople',
            },
        ),
    ]
