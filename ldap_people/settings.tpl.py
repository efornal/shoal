# -*- coding: utf-8 -*-

# =================================\
# ldap configuration
LDAP_SERVER = 'ldap://ldap_host:389'
LDAP_DN = 'dc=*,dc=*,dc=*,dc=*'

# Organizational Unit for Person
LDAP_GROUP  = 'Group' # ou=Entry
LDAP_PEOPLE = 'People' # ou=Entry

LDAP_USERNAME='username'
LDAP_PASSWORD='password'

#
# Maximum limit of results to be taken as error
LDAP_SIZE_LIMIT=100
#
# If specified, add the ObjectClass to the search condition of ldap
LDAP_FILTER_OBJECT_CLASS=[]
#
# Domain name used to identify the institutional mail of an alternative
# Ej: the (LDAP DN)
LDAP_DOMAIN_MAIL=''

# Performs filtering to obtain LDAP groups
# min group_id (group_id>= 500) for ldap search filter
LDAP_GROUP_MIN_VALUE = 500 
# =================================/
