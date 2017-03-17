from __future__ import unicode_literals
import logging
import ldap
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _

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
    id = models.AutoField(primary_key=True,null=False)
#    username = models.CharField(max_length=200,primary_key=True)
    username = models.CharField(max_length=200)
    person_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    fullname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    office = models.CharField(max_length=200)
    group_id = models.CharField(max_length=200)
    document_number = models.CharField(max_length=200)
#    type_document_number = models.CharField(max_length=200)
#    country_document_number = models.CharField(max_length=200)
    telephone_number = models.CharField(max_length=200)
#    home_telephone_number = models.CharField(max_length=200)
    
    class Meta:
        managed = False
        verbose_name = _('LdapPerson')
        verbose_name_plural = _('LdapPeople')
        db_table = 'app_ldapperson'

    def __unicode__(self):
        return self.username

    
    @classmethod
    def ldap_udn_for( cls, ldap_user_name ):
        return "uid=%s,ou=%s,%s" % ( ldap_user_name,
                                     settings.LDAP_PEOPLE,
                                     settings.LDAP_DN )

    def ldap_update(self, person):
        logging.warning("UPDATE::::{}".format(person))

        try:
            update_person = [( ldap.MOD_REPLACE, 'telephoneNumber',
                               str(person['telephone_number']) or None),
                             ( ldap.MOD_REPLACE, 'physicalDeliveryOfficeName',
                               str(person['office']) or None)]

            udn = LdapPerson.ldap_udn_for( person['username'] )
            logging.warning( "Updated ldap user data for {} \n".format(update_person))
            LdapConn.new_user().modify_s(udn, update_person)
        except ldap.LDAPError, e:
            logging.error( "Error updating ldap user data for {} \n".format(update_person))
            logging.error( e )


    @classmethod
    def search_by_uid(cls, uid):
        ldap_condition = "(uid=*{}*)".format( uid )
        retrieve_attributes = None
        ldap_result = LdapConn.new().search_s("ou={},{}".format(settings.LDAP_PEOPLE,
                                                                settings.LDAP_DN),
                                              ldap.SCOPE_SUBTREE,
                                              ldap_condition,
                                              retrieve_attributes )
        
        return LdapPerson.ldap_to_obj(ldap_result)


    @classmethod
    def get_by_uid(cls, uid):
        ldap_condition = "(uid={})".format( uid )
        retrieve_attributes = None
        ldap_result = LdapConn.new_user().search_s("ou={},{}".format(settings.LDAP_PEOPLE,
                                                                     settings.LDAP_DN),
                                                   ldap.SCOPE_SUBTREE,
                                                   ldap_condition)
        p=LdapPerson.ldap_to_obj(ldap_result)[0]
        return p
        # cn_found=[]
#        for dn,entry in ldap_result:
        #     person = {}
        #     if 'cn' in entry and entry['cn'][0]:
        #         person.update({'name': entry['cn'][0]})
        #     else:
        #         person.update({'name': ''})

        #     cn_found.append(person)
                                                   
        # return cn_found



                              
#        return LdapPerson.ldap_to_obj(ldap_result)    

    
    @classmethod
    def ldap_to_obj(cls, ldap_result):
        cn_found = []
        
        for dn,entry in ldap_result:
            person = LdapPerson()

            if 'uid' in entry and entry['uid'][0]:
                person.username = entry['uid'][0]

            if 'cn' in entry and entry['cn'][0]:
                person.full_name = entry['cn'][0]

            if 'givenName' in entry and entry['givenName'][0]:
                person.name = entry['givenName'][0]

            # if 'paisdoc' in entry and entry['paisdoc'][0]:
            #     person.country_document_number = entry['paisdoc'][0]

            if 'numdoc' in entry and entry['numdoc'][0]:
                person.document_number = entry['numdoc'][0]

            # if 'tipodoc' in entry and entry['tipodoc'][0]:
            #     person.type_document_number = entry['tipodoc'][0]

            if 'gidNumber' in entry and entry['gidNumber'][0]:
                person.group_id = entry['gidNumber'][0]

            if 'uidNumber' in entry and entry['uidNumber'][0]:
                person.person_id = entry['uidNumber'][0]
                
            if 'sn' in entry and entry['sn'][0]:                
                person.surname = entry['sn'][0]
                
            if 'mail' in entry and entry['mail'][0]:                
                person.email = entry['mail'][0]
                
            if 'physicalDeliveryOfficeName' in entry \
               and entry['physicalDeliveryOfficeName'][0]:                
                person.office = entry['physicalDeliveryOfficeName'][0]
                
            if 'telephoneNumber' in entry and entry['telephoneNumber'][0]:                
                person.telephone_number = entry['telephoneNumber'][0]

            # if 'homePhone' in entry and entry['homePhone'][0]:                
            #     person.home_telephone_number = entry['homePhone'][0]
                
            cn_found.append(person)
                
        return cn_found

