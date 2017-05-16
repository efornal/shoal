# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# =================================\
# ldap configuration
LDAP_SERVER = 'ldap://ldap_host:389'
LDAP_DN = 'dc=*,dc=*,dc=*,dc=*'

# Organizational Unit for Person
LDAP_GROUP  = 'Group' # ou=Entry
LDAP_PEOPLE = 'People' # ou=Entry

LDAP_USERNAME='username'
LDAP_PASSWORD='password'

