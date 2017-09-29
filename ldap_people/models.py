# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.db import models
import ldap
from django.conf import settings
from django.utils.translation import ugettext as _
from collections import OrderedDict
from django.core.exceptions import ValidationError


class LdapConn():
    
    @classmethod
    def new_anon(cls):
        try:
            connection = ldap.initialize( LdapConn.ldap_server() )
            connection.simple_bind_s()
            return connection
        except ldap.LDAPError, e:
            logging.error("Could not connect to the Ldap server: '{}'" \
                          .format(LdapConn.ldap_server()))
            logging.error(e)
            raise

    @classmethod
    def new_auth(cls, username, password):
        try:
            connection = ldap.initialize( LdapConn.ldap_server() )
            connection.simple_bind_s( "cn={},{}".format( str(username), \
                                                         str(LdapConn.ldap_dn())),  \
                                      str(password) )
            return connection
        except ldap.LDAPError, e:
            logging.error("Could not connect to the Ldap server: '{}'" \
                          .format(LdapConn.ldap_server()))
            logging.error(e)
            raise
        
    @classmethod
    def new(cls):
        return LdapConn.new_auth( LdapConn.ldap_username(), LdapConn.ldap_password() )


    @classmethod
    def ldap_search(cls, condition, attributes=[] ):
        retrieve_attributes = [str(x) for x in attributes]
        ldap_result = []
        try:
            ldap_result = LdapConn.new().search_ext_s(
                "ou={},{}".format(LdapPerson.ldap_ou(),LdapConn.ldap_dn()),
                ldap.SCOPE_SUBTREE,
                condition,
                retrieve_attributes)

        except ldap.TIMEOUT, e:
            logging.error( "Timeout exception {} \n".format(e))
            return None
        except ldap.SIZELIMIT_EXCEEDED, e:
            logging.error( "Size limit exceeded exception {} \n".format(e))
            return None
        except ldap.LDAPError, e:
            logging.error( e )

        return ldap_result
    
    @classmethod
    def ldap_dn(self):
        if hasattr(settings, 'LDAP_DN'):
            return settings.LDAP_DN
        return None

    @classmethod
    def ldap_server(self):
        if hasattr(settings, 'LDAP_SERVER'):
            return settings.LDAP_SERVER
        return None

    @classmethod
    def ldap_password(self):
        if hasattr(settings, 'LDAP_PASSWORD'):
            return settings.LDAP_PASSWORD
        return None

    @classmethod
    def ldap_username(self):
        if hasattr(settings, 'LDAP_USERNAME'):
            return settings.LDAP_USERNAME
        return None


    
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
    host_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('host_name'))
    
    class Meta:
        managed = False
        verbose_name = _('LdapPerson')
        verbose_name_plural = _('LdapPeople')
        db_table = 'ldap_people_ldapperson'
        
    def __unicode__(self):
        return self.username

    
    def __init__(self, *args, **kwargs):
        super(LdapPerson, self).__init__(*args, **kwargs)


    @classmethod
    def ldap_size_limit(self):
        if hasattr(settings, 'LDAP_SIZE_LIMIT'):
            return settings.LDAP_SIZE_LIMIT
        return 100


    @classmethod
    def ldap_ou(self):
        if hasattr(settings, 'LDAP_PEOPLE'):
            return settings.LDAP_PEOPLE
        return None

    
    @classmethod
    def ldap_attrs(cls):
        return ['uid','cn','sn','givenName',
                'paisdoc','numdoc','tipodoc',
                'gidNumber','uidNumber','mail',
                'telephoneNumber','homePhone',
                'employeeType','physicalDeliveryOfficeName',
                'departmentNumber','businessCategory','host']

    
    @classmethod
    def search_ldap_attrs(cls):
        return ['uid','givenName','sn',
                'departmentNumber','businessCategory','employeeType',
                'telephoneNumber','physicalDeliveryOfficeName','mail','host']

        
    @classmethod
    def ldap_udn_for( cls, ldap_user_name ):
        return "uid=%s,ou=%s,%s" % ( ldap_user_name,
                                     LdapPerson.ldap_ou(),
                                     LdapConn.ldap_dn())

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

    
    def save(self, *args, **kwargs):
        """Guarda determinados datos de la persona en LDAP """
        upd_person = []
        new_office = None
        curr_person = LdapPerson.get_by_uid(self.username)
        if self.telephone_number is not None:
            if self.telephone_number:
                upd_person.append(( ldap.MOD_REPLACE,
                                    'telephoneNumber',
                                    str(self.telephone_number)))
            else:
                upd_person.append(( ldap.MOD_DELETE,
                                    'telephoneNumber', None))
                          
        if self.home_telephone_number is not None:
            if self.home_telephone_number:
                upd_person.append(( ldap.MOD_REPLACE,
                                    'homePhone',
                                    str(self.home_telephone_number)))
            else:
                upd_person.append(( ldap.MOD_DELETE,
                                    'homePhone',None))

        if self.floor is not None:
            if self.floor:
                upd_person.append(( ldap.MOD_REPLACE,
                                    'departmentNumber',
                                    str(self.floor)))
            else:
                upd_person.append(( ldap.MOD_DELETE,
                                    'departmentNumber',None))
                
        if self.area is not None:
            if self.area:
                upd_person.append(( ldap.MOD_REPLACE,
                                    'businessCategory',
                                    str(self.area)))
            else:
                upd_person.append(( ldap.MOD_DELETE,
                                    'businessCategory',None))

        if self.position is not None:
            if self.position:
                upd_person.append(( ldap.MOD_REPLACE,
                                    'employeeType',
                                    str(self.position)))
            else:
                upd_person.append(( ldap.MOD_DELETE,
                                    'employeeType',None))

        if self.host_name is not None:
            if self.host_name:
                upd_person.append(( ldap.MOD_REPLACE,
                                    'host',
                                    str(self.host_name)))
            else:
                upd_person.append(( ldap.MOD_DELETE,
                                    'host',None))

        if self.group_id:
            if int(self.group_id) < LdapGroup.ldap_min_gid_value():
                logging.error(_('setting_group_must_be_greater') \
                              % {'group':self.group_id,'value':LdapGroup.ldap_min_gid_value()})
            if int(curr_person.group_id) < LdapGroup.ldap_min_gid_value():
                logging.error(_('changing_group_must_be_greater') \
                              % {'group':curr_person.group_id,'value':LdapGroup.ldap_min_gid_value()})
            elif int(self.group_id) in LdapGroup._skip_groups():
                logging.error(_('setting_group_do_not_allow_edit') \
                              % {'group':self.group_id,'value':LdapGroup._skip_groups()})
            elif int(curr_person.group_id) in LdapGroup._skip_groups():
                logging.error(_('changing_group_do_not_allow_edit') \
                              % {'group':curr_person.group_id,'value':LdapGroup._skip_groups()})
            else:
                upd_person.append((ldap.MOD_REPLACE,
                                   'gidNumber',
                                   str(self.group_id)))
                
        if self.office:
            new_office = self.office
        elif self.other_office:
            new_office = self.other_office
            
        if new_office is not None:
            upd_person.append((ldap.MOD_REPLACE,
                               'physicalDeliveryOfficeName',
                               str(new_office)))

        if self.email:
            mails = []
            mails.append(str(self.email))
            if self.alternative_email:
                mails.append(str(self.alternative_email))
                upd_person.append((ldap.MOD_REPLACE,'mail',mails))
                

        udn = LdapPerson.ldap_udn_for( str(self.username) )
        logging.warning( "Updating ldap user data...\n")

        for upd in upd_person:
            try:
                logging.warning("updating.. {}".format(upd))
                LdapConn.new().modify_s(udn, [upd])                
            except ldap.LDAPError, e:
                logging.error( e )

        try:
            curr_groups = [str(x.group_id) for x in LdapGroup.groups_by_uid(self.username)]
            if self.group_id and (self.group_id not in curr_groups) and \
               (curr_person.group_id != self.group_id):
                logging.warning('Adding user as a member of the new primary group..')
                LdapGroup.add_member_to( self.username, self.group_id )

            if (curr_person.group_id and self.group_id) and \
               (curr_person.group_id != self.group_id): # update members!
                logging.warning('Removing user as a member from the previous parent group..')
                LdapGroup.remove_member_of_group( self.username, curr_person.group_id )
        except ValidationError, e:
            raise ValidationError( e )
        except ldap.LDAPError, e:
            logging.error( e )


    @classmethod
    def search_by_uid(cls, uid):
        ldap_condition = "(uid=*{}*)".format( uid )
        ldap_condition = LdapPerson.compose_ldap_filter(ldap_condition)
        attributes = LdapPerson.search_ldap_attrs()
        retrieve_attributes = [str(x) for x in attributes]
        ldap_result = []
            
        try:
            ldap_result = LdapConn.new().search_ext_s(
                "ou={},{}".format(LdapPerson.ldap_ou(),
                                  LdapConn.ldap_dn()),
                ldap.SCOPE_SUBTREE,
                ldap_condition,
                retrieve_attributes,
                sizelimit=LdapPerson.ldap_size_limit())
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
    def all(cls):
        ldap_condition = "(uid=*)"
        ldap_condition = "(|{})".format( ldap_condition )
        ldap_condition = LdapPerson.compose_ldap_filter(ldap_condition)
        retrieve_attributes = [str(x) for x in LdapPerson.search_ldap_attrs()]
        ldap_result = []
        logging.error(ldap_condition)
        try:
            ldap_result = LdapConn.new().search_ext_s(
                "ou={},{}".format(LdapPerson.ldap_ou(),LdapConn.ldap_dn()),
                ldap.SCOPE_SUBTREE,
                ldap_condition,
                retrieve_attributes)
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
            
        try:
            result = LdapConn.new().search_ext_s(
                "ou={},{}".format(LdapPerson.ldap_ou(),LdapConn.ldap_dn()),
                ldap.SCOPE_SUBTREE,
                ldap_condition,
                retrieve_attributes,
                sizelimit = LdapPerson.ldap_size_limit())
            ldap_result = LdapPerson.ldap_to_obj(result)
        except ldap.TIMEOUT, e:
            logging.error( "Timeout exception {} \n".format(e))
            ldap_result = None
        except ldap.SIZELIMIT_EXCEEDED, e:
            logging.error( "Size limit exceeded exception {} \n".format(e))
            ldap_result = None
        except ldap.LDAPError, e:
            logging.error( e )
            ldap_result = None

        return ldap_result

    
    @classmethod
    def search_by_office(cls, office_name):
        ldap_condition = "(physicalDeliveryOfficeName=*{}*)".format( office_name )
        ldap_condition = "(|{})".format( ldap_condition )
        ldap_condition = LdapPerson.compose_ldap_filter(ldap_condition)
        retrieve_attributes = [str(x) for x in LdapPerson.search_ldap_attrs()]
        ldap_result = []
        logging.error( ldap_condition)
        try:
            result = LdapConn.new().search_ext_s(
                "ou={},{}".format(LdapPerson.ldap_ou(),LdapConn.ldap_dn()),
                ldap.SCOPE_SUBTREE,
                ldap_condition,
                retrieve_attributes,
                sizelimit = LdapPerson.ldap_size_limit())
            ldap_result = LdapPerson.ldap_to_obj(result)
        except ldap.TIMEOUT, e:
            logging.error( "Timeout exception {} \n".format(e))
            ldap_result = None
        except ldap.SIZELIMIT_EXCEEDED, e:
            logging.error( "Size limit exceeded exception {} \n".format(e))
            ldap_result = None
        except ldap.LDAPError, e:
            logging.error( e )
            ldap_result = None

        return ldap_result


    @classmethod
    def by_offices(cls):
        ldap_condition = ""
        #ldap_condition = "(|{})".format( ldap_condition )
        ldap_condition = LdapPerson.compose_ldap_filter(ldap_condition)
        attributes = ['uid','telephoneNumber','physicalDeliveryOfficeName',]
        retrieve_attributes = [str(x) for x in  LdapPerson.search_ldap_attrs()]
        ldap_result = []
            
        try:
            result = LdapConn.new().search_ext_s(
                "ou={},{}".format(LdapPerson.ldap_ou(),LdapConn.ldap_dn()),
                ldap.SCOPE_SUBTREE,
                ldap_condition,
                retrieve_attributes)
            ldap_result = LdapPerson.ldap_to_obj(result)
        except ldap.TIMEOUT, e:
            logging.error( "Timeout exception {} \n".format(e))
            ldap_result = None
        except ldap.SIZELIMIT_EXCEEDED, e:
            logging.error( "Size limit exceeded exception {} \n".format(e))
            ldap_result = None
        except ldap.LDAPError, e:
            logging.error( e )
            ldap_result = None

        return ldap_result

    
    @classmethod
    def get_by_uid(cls, uid):
        ldap_condition = "(uid={})".format( str(uid) )
        ldap_condition = LdapPerson.compose_ldap_filter(ldap_condition)
        retrieve_attributes = [str(x) for x in LdapPerson.ldap_attrs()]
        ldap_result = None
        try:
            ldap_result = LdapConn.new().search_s(
                "ou={},{}".format(LdapPerson.ldap_ou(),LdapConn.ldap_dn()),
                ldap.SCOPE_SUBTREE,
                ldap_condition,
                retrieve_attributes)
            ldap_result = LdapPerson.ldap_to_obj(ldap_result)[0]
        except ldap.LDAPError, e:
            logging.error( e )

        return ldap_result


    @classmethod
    def get_auth_by_uid(cls, uid):
        """
        Retorna PersonaLdap con datos de authenticación
        Usado luego para autenticar las peticiones a Ldap por usuario
        """
        ldap_condition = "(uid={})".format( str(uid) )
        ldap_condition = LdapPerson.compose_ldap_filter(ldap_condition)
        attributes = LdapPerson.ldap_attrs() + ['username','userPassword']
        retrieve_attributes = [str(x) for x in attributes]
        ldap_result = None
        try:
            ldap_result = LdapConn.new().search_s(
                "ou={},{}".format(LdapPerson.ldap_ou(),LdapConn.ldap_dn()),
                ldap.SCOPE_SUBTREE,
                ldap_condition,
                retrieve_attributes)
            ldap_result = LdapPerson.ldap_to_obj(ldap_result)[0]
        except ldap.LDAPError, e:
            logging.error( e )

        return ldap_result

    
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

            if 'userPassword' in entry and entry['userPassword'][0]:
                person.password = entry['userPassword'][0]

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

            if 'mail' in entry and len(entry['mail']) > 0:
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

            if 'businessCategory' in entry and entry['businessCategory'][0]:
                person.area = entry['businessCategory'][0]

            if 'employeeType' in entry and entry['employeeType'][0]:
                person.position = entry['employeeType'][0]

            if 'host' in entry and entry['host'][0]:
                person.host_name = entry['host'][0]

            cn_found.append(person)

        return sorted(cn_found, key=lambda person: person.fullname)


    @classmethod
    def available_attribute_values(cls, attribute_name):
        condition = "(uid=*)"
        condition = "(|{})".format( condition )
        condition = LdapPerson.compose_ldap_filter(condition)
        attributes = [attribute_name]
        available_values = []
        ldap_result = LdapConn.ldap_search(condition,attributes)
        try:
            for dn,entry in ldap_result:
                if attribute_name in entry \
                   and entry[attribute_name][0] \
                   and not (entry[attribute_name][0] in available_values):
                    available_values.append(entry[attribute_name][0])
        except Exception, e:
            logging.error( e )

        return available_values

    @classmethod
    def available_floors(cls):
        return LdapPerson.available_attribute_values('departmentNumber')
    
    @classmethod
    def available_employee_types(cls):
        return LdapPerson.available_attribute_values('employeeType')

    @classmethod
    def available_areas(cls):
        return LdapPerson.available_attribute_values('businessCategory')

    @classmethod
    def available_floors(cls):
        return LdapPerson.available_attribute_values('departmentNumber')


    
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
    def ldap_ou(self):
        if hasattr(settings, 'LDAP_GROUP'):
            return settings.LDAP_GROUP
        return None

    @classmethod
    def ldap_min_gid_value(self):
        if hasattr(settings, 'LDAP_GROUP_MIN_VALUE'):
            return settings.LDAP_GROUP_MIN_VALUE
        return None
    
    @classmethod
    def ldap_attrs(cls):
        return ['gidNumber','cn'] # id first!

    @classmethod
    def _skip_groups(cls):
        groups = []
        if hasattr(settings, 'LDAP_GROUP_SKIP_VALUES') \
           and len(settings.LDAP_GROUP_SKIP_VALUES)>0:
            groups = settings.LDAP_GROUP_SKIP_VALUES
        return groups
            
    @classmethod
    def _skip_groups_filter(cls):
        filters = ''
        for gid in LdapGroup._skip_groups():
            filters += '(!({}={}))'.format(settings.LDAP_GROUP_FIELDS[0],gid)
        return filters

    @classmethod
    def all(cls):
        rows = []
        ldap_result = []
        retrieve_attributes = [str(x) for x in LdapGroup.ldap_attrs()]
        ldap_condition = "(&(cn=*)({}>={}))".format(settings.LDAP_GROUP_FIELDS[0],
                                                      settings.LDAP_GROUP_MIN_VALUE)

        try:
            ldap_result = LdapConn.new().search_s( "ou={},{}".format(LdapGroup.ldap_ou(),
                                                                     LdapConn.ldap_dn()),
                                                        ldap.SCOPE_SUBTREE,
                                                        ldap_condition,
                                                        retrieve_attributes )
        except ldap.LDAPError, e:
            logging.error( e )
        
        return LdapGroup.ldap_to_obj(ldap_result)

    
    @classmethod
    def members_of(cls, gid):
        ldap_result = []
        retrieve_attributes = [str('memberUid')]
        ldap_condition = "(cn={})" .format(gid)
        members = []
        try:
            ldap_result = LdapConn.new().search_s("ou={},{}".format(LdapGroup.ldap_ou(),
                                                                    LdapConn.ldap_dn()),
                                                  ldap.SCOPE_SUBTREE,
                                                  ldap_condition,
                                                  retrieve_attributes )
            for dn,entry in ldap_result:
                members = entry['memberUid']
                
        except ldap.LDAPError, e:
            logging.error( e )
        
        return members
            
    
    @classmethod
    def groups_by_uid(cls, uid):
        ldap_result = []
        retrieve_attributes = [str(x) for x in  LdapGroup.ldap_attrs()]
        ldap_condition = "(&(cn=*)(memberUid={0})({1}>={2}))" \
            .format( uid,
                     retrieve_attributes[0],
                     LdapGroup.ldap_min_gid_value())
        try:
            ldap_result = LdapConn.new().search_s("ou={},{}".format(LdapGroup.ldap_ou(),
                                                                    LdapConn.ldap_dn()),
                                                  ldap.SCOPE_SUBTREE,
                                                  ldap_condition,
                                                  retrieve_attributes )
        except ldap.LDAPError, e:
            logging.error( e )
        
        return LdapGroup.ldap_to_obj(ldap_result)
    
            
    @classmethod
    def add_member_to( cls,  ldap_username, group_id ):
        
        if int(group_id) < LdapGroup.ldap_min_gid_value():
            error_message = _('adding_group_must_be_greater') \
                            % {'group':group_id,'value':LdapGroup.ldap_min_gid_value()}
            logging.error("Error adding group {}, must be greater than {}" \
                          .format(group_id,LdapGroup.ldap_min_gid_value()))
            raise ValidationError(error_message)

        if int(group_id) in LdapGroup._skip_groups():
            error_message = _('adding_group_do_not_allow_editing') \
                            % {'group':group_id,'value':LdapGroup._skip_groups()}
            logging.error("Error adding group {}, the settings do not allow editing" \
                          " of the following groups: {}" \
                          .format( group_id,LdapGroup._skip_groups()))
            raise ValidationError(error_message)

        ldap_username = str(ldap_username)
        update_group = [( ldap.MOD_ADD, 'memberUid', ldap_username )]
        
        try:
            group_name = LdapGroup.cn_group_by_gid(group_id)
            gdn = "cn={},ou={},{}".format ( group_name,
                                            LdapGroup.ldap_ou(),
                                            LdapConn.ldap_dn() )
            LdapConn.new().modify_s(gdn, update_group)
            logging.warning("Added new member {} in ldap group: {} \n" \
                            .format(ldap_username,group_name))
        except ldap.LDAPError, e:
            logging.error( "Error adding member {} in ldap group: {} \n" \
                           .format(ldap_username,group_name))
            logging.error( e )

            
    @classmethod
    def add_member_in_groups( cls,  ldap_username, group_ids ):
        errors = []
        for group_id in group_ids:
            try:
                LdapGroup.add_member_to(ldap_username,group_id)
            except Exception, e:
                errors.append(e)
        if errors:
            raise ValidationError(errors)  

        
    @classmethod
    def remove_member_of_groups( cls,  ldap_username, group_ids ):
        errors = []
        for group_id in group_ids:
            try:
                LdapGroup.remove_member_of_group(ldap_username,group_id)
            except Exception, e:
                errors.append(e)
        if errors:
            raise ValidationError(errors)  
            

    @classmethod
    def remove_member_of_group( cls,  ldap_username, group_id ):

        if int(group_id) < LdapGroup.ldap_min_gid_value():
            error_message = _('removing_group_must_be_greater') \
                            % {'group':group_id,'value':LdapGroup.ldap_min_gid_value()}
            logging.error("Error removing group {}, must be greater than {}" \
                          .format(group_id,LdapGroup.ldap_min_gid_value()))
            raise ValidationError(error_message)

        if int(group_id) in LdapGroup._skip_groups():
            error_message = _('removing_group_do_not_allow_editing') \
                            % {'group':group_id,'value':LdapGroup._skip_groups()}
            logging.error("Error removing group {}, the settings do not allow editing" \
                          " of the following groups: {}" \
                          .format( group_id, LdapGroup._skip_groups()))
            raise ValidationError(error_message)

        ldap_username = str(ldap_username)
        group_name = LdapGroup.cn_group_by_gid(group_id)

        if not (ldap_username and group_name):
            logging.error("Error deleting group %s of member: %s. Missing parameter.\n" \
                          .format(group_name,ldap_username))
            return
            
        delete_member = [(ldap.MOD_DELETE , 'memberUid', ldap_username )]
        try:
            gdn = "cn={},ou={},{}".format( group_name,
                                           LdapGroup.ldap_ou(),
                                           LdapConn.ldap_dn() )
            LdapConn.new().modify_s(gdn,delete_member)
            logging.warning("Removed member {} of group {} \n" \
                         .format(ldap_username,group_name))
        except ldap.LDAPError, e:
            logging.error( "Error deleting member {} of group: {} \n" \
                           .format(ldap_username,group_name))
            logging.error( e )

            
    @classmethod
    def update_member_in_groups( cls,  ldap_username, new_groups ):
        curr_groups = [str(x.group_id) for x in LdapGroup.groups_by_uid(ldap_username)]
        remove_groups = [item for item in curr_groups if item not in new_groups]
        add_groups = [item for item in new_groups if item not in curr_groups]
        try:
            LdapGroup.add_member_in_groups( ldap_username, add_groups )
            LdapGroup.remove_member_of_groups (ldap_username, remove_groups )
        except Exception, e:
            raise ValidationError(e)  


        
    @classmethod
    def cn_group_by_gid(cls, gid):
        ldap_condition = "(gidNumber={})".format(str(gid))
        cn_found = None
        r = LdapConn.new().search_s("ou={},{}".format(LdapGroup.ldap_ou(),
                                                      LdapConn.ldap_dn()),
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

    def __str__(self):
        return self.name

    
class LdapOffice(models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False)
    name = models.CharField(
        max_length=200,
        null=False,
        verbose_name=_('name'))
    
    class Meta:
#        managed = False
        db_table = 'ldap_people_ldapoffices'
        verbose_name = _('LdapOffice')
        verbose_name_plural = _('LdapOffices')
        
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    @classmethod
    def all(cls):
        ldap_condition = "(uid=*)"
        ldap_condition = "(|{})".format( ldap_condition )
        ldap_condition = LdapPerson.compose_ldap_filter(ldap_condition)
        attrs = ['physicalDeliveryOfficeName']
        retrieve_attributes = [str(x) for x in attrs]
        ldap_result = []
        try:
            ldap_result = LdapConn.new().search_ext_s(
                "ou={},{}".format(LdapPerson.ldap_ou(),LdapConn.ldap_dn()),
                ldap.SCOPE_SUBTREE,
                ldap_condition,
                retrieve_attributes)
        except ldap.TIMEOUT, e:
            logging.error( "Timeout exception {} \n".format(e))
            return None
        except ldap.SIZELIMIT_EXCEEDED, e:
            logging.error( "Size limit exceeded exception {} \n".format(e))
            return None
        except ldap.LDAPError, e:
            logging.error( e )

        return LdapOffice.ldap_to_obj(ldap_result)

    
    @classmethod    
    def telephones(self):
        offices = {}
        try:
            people = LdapPerson.by_offices()
            for person in people:
                if person.office is not None \
                   and person.telephone_number is not None:
                    curr_phone = offices.get('{}'.format(person.office))
                    if curr_phone and person.telephone_number not in curr_phone:
                        curr_phone = '{}, {}'.format( curr_phone,person.telephone_number)
                    else:
                        curr_phone = '{}'.format( person.telephone_number)
                    offices.update({'{}'.format(person.office):'{}'.format(curr_phone)})

            return OrderedDict(sorted(offices.items(), key=lambda t: t[0]))
        except Exception, e:
            logging.error(e)

        return offices

    @classmethod
    def ldap_to_obj(cls, ldap_result):
        cn_found = []
        for dn,entry in ldap_result:
            if 'physicalDeliveryOfficeName' in entry \
               and entry['physicalDeliveryOfficeName'][0] \
               and entry['physicalDeliveryOfficeName'][0] not in cn_found:
                cn_found.append(entry['physicalDeliveryOfficeName'][0])

        office_names = []
        office = None
        for office_name in sorted(cn_found):
            office = LdapOffice()
            office.name = office_name
            office_names.append(office)
        
        return office_names
