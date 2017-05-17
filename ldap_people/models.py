# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.db import models
import ldap
from django.conf import settings
from django.utils.translation import ugettext as _

class LdapConn():
    
    @classmethod
    def new_anon(cls):
        try:
            connection = ldap.initialize( settings.LDAP_SERVER )
            connection.simple_bind_s()
            return connection
        except ldap.LDAPError, e:
            logging.error("Could not connect to the Ldap server: '{}'" \
                          .format(settings.LDAP_SERVER))
            logging.error(e)
            raise

        
    @classmethod
    def new(cls):
        try:
            connection = ldap.initialize( settings.LDAP_SERVER )
            connection.simple_bind_s( "cn={},{}" \
                                      .format( settings.LDAP_USERNAME, \
                                               settings.LDAP_DN ), \
                                      settings.LDAP_PASSWORD )
            return connection
        except ldap.LDAPError, e:
            logging.error("Could not connect to the Ldap server: '{}'" \
                          .format(settings.LDAP_SERVER))
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
        return ['uid','cn','sn','givenName',
                'paisdoc','numdoc','tipodoc',
                'gidNumber','uidNumber','mail',
                'telephoneNumber','homePhone',
                'employeeType','physicalDeliveryOfficeName',
                'departmentNumber','destinationIndicator',]

    
    @classmethod
    def search_ldap_attrs(cls):
        return ['uid','givenName','sn',
                'telephoneNumber','physicalDeliveryOfficeName','mail']

        
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
        
    
    def save(self):
        try:
            ldap_person = [( ldap.MOD_REPLACE, 'telephoneNumber',
                               str(self.telephone_number) or None),
                             ( ldap.MOD_REPLACE, 'physicalDeliveryOfficeName',
                               str(self.office) or None),
                             ( ldap.MOD_REPLACE, 'gidNumber',
                               str(self.group_id) or None),
                             ( ldap.MOD_REPLACE, 'departmentNumber',
                               str(self.floor) or None),
                             ( ldap.MOD_REPLACE, 'destinationIndicator',
                               str(self.area) or None),
                             ( ldap.MOD_REPLACE, 'employeeType',
                               str(self.position) or None),]

            if self.office:
                new_office = self.office
            elif self.other_office:
                new_office = self.other_office

            ldap_person.append((ldap.MOD_REPLACE,
                                'physicalDeliveryOfficeName',
                                str(new_office)))

            if self.email:
                mails = []
                mails.append(str(self.email))
                if self.alternative_email:
                    mails.append(str(self.alternative_email))
                ldap_person.append((ldap.MOD_REPLACE,'mail',mails))
                
            udn = LdapPerson.ldap_udn_for( str(self.username) )

            logging.warning( "Updated ldap user data for {} \n".format(ldap_person))
            LdapConn.new().modify_s(udn, ldap_person)
            
        except ldap.LDAPError, e:
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
            ldap_result = LdapConn.new().search_ext_s(
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
        retrieve_attributes = [str(x) for x in LdapPerson.search_ldap_attrs()]
        ldap_result = []
        size_limit = 100

        if hasattr(settings, 'LDAP_SIZE_LIMIT'):
            size_limit = settings.LDAP_SIZE_LIMIT
            
        try:
            ldap_result = LdapConn.new().search_ext_s(
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
            ldap_result = LdapConn.new().search_s(
                "ou={},{}".format(settings.LDAP_PEOPLE,
                                  settings.LDAP_DN),
                ldap.SCOPE_SUBTREE,
                ldap_condition,
                retrieve_attributes)
        except ldap.LDAPError, e:
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

            if 'mail' in entry and entry['mail'][0]:                
                for mail in entry['mail']:
                    if ldap_domain_mail and ldap_domain_mail in mail:
                        person.email = mail
                    else:
                        person.alternative_email = mail
                
            if 'givenName' in entry and entry['givenName'][0]:
                person.name = "%s" % entry['givenName'][0]
                #person.name = "%s" % entry['givenName'][0]

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

        return sorted(cn_found, key=lambda person: person.fullname)


    
class LdapGroup(models.Model):
    group_id = models.IntegerField()
    name     = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
        managed = False
        
    def __unicode__(self):
        return self.name

    
    @classmethod
    def ldap_attrs(cls):
        return ['gidNumber','cn'] # id first!

    
    @classmethod
    def all(cls):
        rows = []
        ldap_result = []
        attributes = LdapGroup.ldap_attrs()
        retrieve_attributes = [str(x) for x in attributes]

        ldap_condition = "(&(cn=*)({}>={}))".format( retrieve_attributes[0],
                                                     settings.LDAP_GROUP_MIN_VALUE)
        try:
            ldap_result = LdapConn.new().search_s( "ou={},{}".format(settings.LDAP_GROUP,
                                                                          settings.LDAP_DN),
                                                        ldap.SCOPE_SUBTREE,
                                                        ldap_condition,
                                                        retrieve_attributes )
        except ldap.LDAPError, e:
            logging.error( e )
        
        return LdapGroup.ldap_to_obj(ldap_result)

            
    
    @classmethod
    def groups_by_uid(cls, uid):
        attributes = LdapGroup.ldap_attrs()
        retrieve_attributes = [str(x) for x in attributes]

        ldap_condition = "(&(cn=*)(memberUid={0})({1}>={2}))" \
            .format( uid,
                     retrieve_attributes[0],
                     settings.LDAP_GROUP_MIN_VALUE)
        cn_found = None

        ldap_result = LdapConn.new().search_s("ou={},{}".format(settings.LDAP_GROUP,
                                                      settings.LDAP_DN),
                                    ldap.SCOPE_SUBTREE,
                                    ldap_condition,
                                    retrieve_attributes )
        
        return LdapGroup.ldap_to_obj(ldap_result)
    
            
    @classmethod
    def add_member_to( cls,  ldap_username, group_id ):
        if group_id < settings.LDAP_GROUP_MIN_VALUE:
            logging.error("Error removing group {}, must be greater than {}" \
                          .format(group_id,settings.LDAP_GROUP_MIN_VALUE))
            return

        ldap_username = str(ldap_username)
        update_group = [( ldap.MOD_ADD, 'memberUid', ldap_username )]
        
        try:
            group_name = LdapGroup.cn_group_by_gid(group_id)
            gdn = "cn={},ou={},{}".format ( group_name,
                                            settings.LDAP_GROUP,
                                            settings.LDAP_DN )
            LdapConn.new().modify_s(gdn, update_group)
            logging.warning("Added new member {} in ldap group: {} \n" \
                            .format(ldap_username,group_name))
        except ldap.LDAPError, e:
            logging.error( "Error adding member {} in ldap group: {} \n" \
                           .format(ldap_username,group_name))
            logging.error( e )

            
    @classmethod
    def add_member_in_groups( cls,  ldap_username, group_ids ):
        for group_id in group_ids:
            LdapGroup.add_member_to(ldap_username,group_id)


    @classmethod
    def remove_member_of_group( cls,  ldap_username, group_id ):

        if group_id < settings.LDAP_GROUP_MIN_VALUE:
            logging.error("Error removing group {}, must be greater than {}" \
                          .format(group_id,settings.LDAP_GROUP_MIN_VALUE))
            return
        ldap_username = str(ldap_username)
        group_name = LdapGroup.cn_group_by_gid(group_id)

        if not (ldap_username and group_name):
            logging.error("Error deleting group %s of member: %s. Missing parameter.\n" \
                          .format(group_name,ldap_username))
            return
            
        delete_member = [(ldap.MOD_DELETE , 'memberUid', ldap_username )]
        try:
            gdn = "cn={},ou={},{}".format( group_name,
                                           settings.LDAP_GROUP,
                                           settings.LDAP_DN )
            LdapConn.new().modify_s(gdn,delete_member)
            logging.warning("Removed member {} of group {} \n" \
                         .format(ldap_username,group_name))
        except ldap.LDAPError, e:
            logging.error( "Error deleting member {} of group: {} \n" \
                           .format(ldap_username,ldap_group))
            logging.error( e )

            
    @classmethod
    def remove_member_of_groups( cls,  ldap_username, group_ids ):
        for group_id in group_ids:
            LdapGroup.remove_member_of_group(ldap_username,group_id)
            

    @classmethod
    def update_member_in_groups( cls,  ldap_username, new_groups ):
        curr_groups = [str(x.group_id) for x in LdapGroup.groups_by_uid(ldap_username)]
        remove_groups = [item for item in curr_groups if item not in new_groups]
        add_groups = [item for item in new_groups if item not in curr_groups]
        LdapGroup.add_member_in_groups( ldap_username, add_groups )
        LdapGroup.remove_member_of_groups (ldap_username, remove_groups )

        
    @classmethod
    def cn_group_by_gid(cls, gid):
        ldap_condition = "(gidNumber={})".format(str(gid))
        cn_found = None
        r = LdapConn.new().search_s("ou={},{}".format(settings.LDAP_GROUP,
                                                      settings.LDAP_DN),
                                    ldap.SCOPE_SUBTREE,
                                    ldap_condition,
                                    [str("cn")])
        for dn,entry in r:
            if 'cn' in entry and entry['cn'][0]:
                cn_found = entry['cn'][0]

        return cn_found

    
    @classmethod
    def ldap_to_obj(cls, ldap_result):
        cn_found = []
        for dn,entry in ldap_result:
            group = LdapGroup()
            if 'gidNumber' in entry and entry['gidNumber'][0]:
                group.group_id = entry['gidNumber'][0]
            if 'cn' in entry and entry['cn'][0]:
                group.name = entry['cn'][0]
            cn_found.append(group)

        return sorted(cn_found, key=lambda group: group.name)


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
