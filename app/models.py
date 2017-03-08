from __future__ import unicode_literals
import logging
import ldap
from django.db import models
from django.conf import settings
# Create your models here.

    
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
    def people_by_uid(cls, uid):
        ldap_condition = "(uid=*{}*)".format( uid )
        cn_found = []

        r = LdapConn.new().search_s("ou={},{}".format(settings.LDAP_PEOPLE, settings.LDAP_DN),
                                    ldap.SCOPE_SUBTREE,
                                    ldap_condition)
        for dn,entry in r:
#            logging.warning(entry)
            person={}
            if 'cn' in entry and entry['cn'][0]:
                person.update({'name': entry['cn'][0]})
            else:
                person.update({'name': ''})
                
            if 'sn' in entry and entry['sn'][0]:                
                person.update({'surname': entry['sn'][0]})
            else:
                person.update({'surname': ''})
                
            if 'mail' in entry and entry['mail'][0]:                
                person.update({'email': entry['mail'][0]})
            else:
                person.update({'email': ''})
                
            if 'physicalDeliveryOfficeName' in entry \
               and entry['physicalDeliveryOfficeName'][0]:                
                person.update({'office': entry['physicalDeliveryOfficeName'][0]})
            else:
                person.update({'office': ''})
                
            if 'telephoneNumber' in entry and entry['telephoneNumber'][0]:                
                person.update({'telephone_number': entry['telephoneNumber'][0]})
            else:
                person.update({'telephone_number': ''})

            cn_found.append(person)
                
        return cn_found
