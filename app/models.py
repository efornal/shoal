# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import ldap
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class LdapConn():

    @classmethod
    def new(cls, ldap_username='', ldap_password=''):
        try:
            connection = ldap.initialize( settings.LDAP_SERVER )
            if ldap_username and ldap_password:
                connection.simple_bind_s( "uid=%s,ou=%s,%s" % ( ldap_username, 
                                                                settings.LDAP_PEOPLE, 
                                                                settings.LDAP_DN ),
                                          ldap_password )
            else:
                connection.simple_bind_s()
                
            return connection

        except ldap.LDAPError, e:
            logging.error("Could not connect to the Ldap server: '%s'" % settings.LDAP_SERVER )
            logging.error(e)
            raise

    @classmethod
    def new_user(cls):
        try:
            connection = ldap.initialize( settings.LDAP_SERVER )
            connection.simple_bind_s( "cn=%s,%s" % ( settings.LDAP_USERNAME, settings.LDAP_DN ),
                                      settings.LDAP_USERPASS )
            return connection

        except ldap.LDAPError, e:
            logging.error("Could not connect to the Ldap server: '%s'" % settings.LDAP_SERVER )
            logging.error(e)
            raise


    
class LdapPerson(models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False)
    username = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('username'))
    person_id = models.CharField(
        max_length=200,
        null=True,
        blank=True)
    name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('name'))
    surname = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('surname'))
    fullname = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('fullname'))
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_('email'))
    alternative_email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_('alternative_email'))
    office = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('office'))
    other_office = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('other_office'))
    group_id = models.CharField(
        max_length=200,
        null=True,
        blank=True)
    document_number = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('document_number'))
    type_document_number = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('type_document_number'))
    country_document_number = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('country_document_number'))
    telephone_number = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('telephone_number'))
    home_telephone_number = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('home_telephone_number'))
    floor = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('floor'))
    area = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('area'))
    position = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('position'))
    
    class Meta:
        managed = False
        verbose_name = _('LdapPerson')
        verbose_name_plural = _('LdapPeople')
        db_table = 'app_ldapperson'

    def __unicode__(self):
        return self.username

    @classmethod
    def ldap_attrs(cls):
        return ['uid',
                'cn',
                'givenName',
                'paisdoc',
                'numdoc',
                'tipodoc',
                'gidNumber',
                'uidNumber',
                'sn',
                'mail',
                'physicalDeliveryOfficeName',
                'telephoneNumber',
                'homePhone',
                'departmentNumber',
                'destinationIndicator',
                'employeeType',]

    @classmethod
    def search_ldap_attrs(cls):
        return ['uid','givenName','sn','telephoneNumber',
                'physicalDeliveryOfficeName','mail']

        
    @classmethod
    def ldap_udn_for( cls, ldap_user_name ):
        return "uid=%s,ou=%s,%s" % ( ldap_user_name,
                                     settings.LDAP_PEOPLE,
                                     settings.LDAP_DN )

    @classmethod
    def compose_ldap_filter ( cls, extra_conditions="",operator='&' ):
        settings_condition = ""
        if hasattr(settings, 'LDAP_FILTER_OBJECT_CLASS'):
            if len(settings.LDAP_FILTER_OBJECT_CLASS) > 0:
                for s in settings.LDAP_FILTER_OBJECT_CLASS:
                    settings_condition += "(objectClass={})".format(s)

                return "({}{}{})".format(operator,
                                         extra_conditions,
                                         settings_condition)
        return extra_conditions
        
    
    def ldap_update(self, person):
        logging.warning("UPDATE::::{}".format(person))
        
        try:
            update_person = [( ldap.MOD_REPLACE, 'telephoneNumber',
                               str(person['telephone_number']) or None),
                             ( ldap.MOD_REPLACE, 'physicalDeliveryOfficeName',
                               str(person['office']) or None),
                             ( ldap.MOD_REPLACE, 'departmentNumber',
                               str(person['floor']) or None),
                             ( ldap.MOD_REPLACE, 'destinationIndicator',
                               str(person['area']) or None),
                             ( ldap.MOD_REPLACE, 'employeeType',
                               str(person['position']) or None),]

            if 'email' in person and person['email']:
                mails = []
                mails.append(str("{}".format(person['email'])))

                if 'alternative_email' in person and person['alternative_email']:
                    mails.append(str("{}".format(person['alternative_email'])))

                update_person.append((ldap.MOD_REPLACE,
                                      'mail',
                                      mails))
            udn = LdapPerson.ldap_udn_for( person['username'] )

            logging.warning( "Updated ldap user data for {} \n".format(update_person))
            LdapConn.new_user().modify_s(udn, update_person)
        except ldap.LDAPError, e:
            logging.error( "Error updating ldap user data for {} \n".format(update_person))
            logging.error( e )


    @classmethod
    def search_by_uid(cls, uid):
        ldap_condition = "(uid=*{}*)".format( uid )
        ldap_condition = LdapPerson.compose_ldap_filter(ldap_condition)
        attributes = LdapPerson.search_ldap_attrs()
        retrieve_attributes = [str(x) for x in attributes]
        ldap_result = []
        size_limit = 100

        if hasattr(settings, 'LDAP_SIZE_LIMIT'):
            size_limit = settings.LDAP_SIZE_LIMIT
            
        try:
            ldap_result = LdapConn.new_user().search_ext_s(
                "ou={},{}".format(settings.LDAP_PEOPLE,
                                  settings.LDAP_DN),
                ldap.SCOPE_SUBTREE,
                ldap_condition,
                retrieve_attributes,
                sizelimit=size_limit)
        except ldap.TIMEOUT, e:
            logging.error( "Timeout exception {} \n".format(e))
            return None
        except ldap.SIZELIMIT_EXCEEDED, e:
            logging.error( "Size limit exceeded exception {} \n".format(e))
            return None
        except ldap.LDAPError, e:
            logging.error( e )

        return LdapPerson.ldap_to_obj(ldap_result)

    
    @classmethod
    def search(cls, text):
        ldap_condition = "(uid=*{}*)".format( text )
        ldap_condition += "(cn=*{}*)".format( text )
        ldap_condition += "(sn=*{}*)".format( text )
        ldap_condition += "(givenName=*{}*)".format( text )
        ldap_condition += "(numdoc=*{}*)".format( text )
        ldap_condition += "(physicalDeliveryOfficeName=*{}*)".format( text )
        ldap_condition += "(telephoneNumber=*{}*)".format( text )
        ldap_condition = "(|{})".format( ldap_condition )
        ldap_condition = LdapPerson.compose_ldap_filter(ldap_condition)
        attributes = LdapPerson.search_ldap_attrs()
        retrieve_attributes = [str(x) for x in attributes]
        ldap_result = []
        size_limit = 100

        if hasattr(settings, 'LDAP_SIZE_LIMIT'):
            size_limit = settings.LDAP_SIZE_LIMIT
            
        try:
            ldap_result = LdapConn.new_user().search_ext_s(
                "ou={},{}".format(settings.LDAP_PEOPLE,
                                  settings.LDAP_DN),
                ldap.SCOPE_SUBTREE,
                ldap_condition,
                retrieve_attributes,
                sizelimit=size_limit)
        except ldap.TIMEOUT, e:
            logging.error( "Timeout exception {} \n".format(e))
            return None
        except ldap.SIZELIMIT_EXCEEDED, e:
            logging.error( "Size limit exceeded exception {} \n".format(e))
            return None
        except ldap.LDAPError, e:
            logging.error( e )

        return LdapPerson.ldap_to_obj(ldap_result)

    
    @classmethod
    def get_by_uid(cls, uid):
        ldap_condition = "(uid={})".format( uid )
        ldap_condition = LdapPerson.compose_ldap_filter(ldap_condition)
        retrieve_attributes = [str(x) for x in LdapPerson.ldap_attrs()]
        ldap_result = []

        try:
            ldap_result = LdapConn.new_user().search_s(
                "ou={},{}".format(settings.LDAP_PEOPLE,
                                  settings.LDAP_DN),
                ldap.SCOPE_SUBTREE,
                ldap_condition,
                retrieve_attributes)
        except ldap.LDAPError, e:
            logging.error( "Error updating ldap user data for {} \n".format(update_person))
            logging.error( e )

        return LdapPerson.ldap_to_obj(ldap_result)[0]


    @classmethod
    def ldap_to_obj(cls, ldap_result):
        cn_found = []
        ldap_domain_mail = ''
        if hasattr(settings, 'LDAP_DOMAIN_MAIL') and settings.LDAP_DOMAIN_MAIL:
            ldap_domain_mail = settings.LDAP_DOMAIN_MAIL
            
        for dn,entry in ldap_result:
            person = LdapPerson()
            if 'uid' in entry and entry['uid'][0]:
                person.username = entry['uid'][0]

            if 'cn' in entry and entry['cn'][0]:
                person.fullname = entry['cn'][0]
            else:
                if 'sn' in entry and entry['sn'][0] and \
                   'givenName' in entry and entry['givenName'][0]:
                    person.fullname = "{}, {}".format(entry['sn'][0],entry['givenName'][0])
                elif 'sn' in entry and entry['sn'][0]:
                    person.fullname = entry['sn'][0]
                elif 'givenName' in entry and entry['givenName'][0]:
                    person.fullname = entry['givenName'][0]
                
            if 'givenName' in entry and entry['givenName'][0]:
                person.name = entry['givenName'][0]

            if 'paisdoc' in entry and entry['paisdoc'][0]:
                person.country_document_number = entry['paisdoc'][0]

            if 'numdoc' in entry and entry['numdoc'][0]:
                person.document_number = entry['numdoc'][0]

            if 'tipodoc' in entry and entry['tipodoc'][0]:
                person.type_document_number = entry['tipodoc'][0]

            if 'gidNumber' in entry and entry['gidNumber'][0]:
                person.group_id = entry['gidNumber'][0]

            if 'uidNumber' in entry and entry['uidNumber'][0]:
                person.person_id = entry['uidNumber'][0]
                
            if 'sn' in entry and entry['sn'][0]:                
                person.surname = entry['sn'][0]
                
            if 'mail' in entry and entry['mail'][0]:                
                for mail in entry['mail']:
                    if ldap_domain_mail and ldap_domain_mail in mail:
                        person.email = mail
                    else:
                        person.alternative_email = mail

            if 'physicalDeliveryOfficeName' in entry \
               and entry['physicalDeliveryOfficeName'][0]:                
                person.office = entry['physicalDeliveryOfficeName'][0]
                
            if 'telephoneNumber' in entry and entry['telephoneNumber'][0]:                
                person.telephone_number = entry['telephoneNumber'][0]

            if 'homePhone' in entry and entry['homePhone'][0]:                
                person.home_telephone_number = entry['homePhone'][0]

            if 'departmentNumber' in entry and entry['departmentNumber'][0]:                
                person.floor = entry['departmentNumber'][0]

            if 'destinationIndicator' in entry and entry['destinationIndicator'][0]:
                person.area = entry['destinationIndicator'][0]

            if 'employeeType' in entry and entry['employeeType'][0]:
                person.position = entry['employeeType'][0]

            cn_found.append(person)

        return cn_found



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

