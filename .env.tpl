## django configuration

APPLICATION_NAME=Internos
APPLICATION_DESC=Internos

DEBUG=True

LOGGING_LEVEL=INFO

BASE_URL=https://base_url

SECRET_KEY=p7p0c223vc98k_qx31op8c18s9&x*1kvott8**zbjc+ec3t%!

ALLOWED_HOSTS=['*']

ADMINS=(("admin", "admin@site.com"),)

MANAGERS=(("Manager Name", "manager@site.com"),)

TIME_ZONE=America/Argentina/Buenos_Aires

LANGUAGE_CODE=es

DEFAULT_CHARSET=utf-8

STATIC_ROOT=/srv/shoal/shared/static

STATIC_URL=/static/

CONTEXT_ROOT=/

CONTEXT_PATH=/srv/shoal

LOGIN_URL=/login

LOGIN_REDIRECT_URL=/

SESSION_COOKIE_NAME=shoalsessionid


# =================================\

## ldap configuration
LDAP_SERVER=ldap://host_ldap:389

# system user authentication - shoal
# with modify permissions on user entries
LDAP_BIND_DN=dc=site,dc=edu,dc=ar
LDAP_BIND_USERNAME=username
LDAP_BIND_PASSWORD=password

# DN of telephone directory users
# They are the users to be displayed in the telephone list of the main page
LDAP_DN_USERS=dc=site,dc=edu,dc=ar

# Authentication of users using the system
LDAP_DN_AUTH_GROUP=ou=Group,dc=site,dc=edu,dc=ar
LDAP_DN_AUTH_USERS=ou=People,dc=site,dc=edu,dc=ar

# Organizational Unit for Person
#LDAP_PEOPLE=People
#LDAP_GROUP=Group

LDAP_GROUP_FIELDS=["gidNumber","cn"]
LDAP_PEOPLE_FIELDS=["uid","cn"]

# Maximum limit of results to be taken as error
LDAP_SIZE_LIMIT=100
#
# If specified, add the ObjectClass to the search condition of ldap
LDAP_FILTER_OBJECT_CLASS=["agente"]
#
# If specified, add the ObjectClass to the search condition of ldap
LDAP_FILTER_MEMBERS_OUT_OF_GROUPS=["users"]
#
# Enable password change functionality
ENABLE_ADMIN_PASSWORD_CHANGE=True
#
# Enable password change functionality
ENABLE_USER_PASSWORD_CHANGE=True
#
# restricts the password change functionality
# for users who are in the indicated groups
RESTRICT_PASSWORD_CHANGE_TO_GROUPS=[]
#
# Domain name used to identify the institutional mail of an alternative
# Ej: the (LDAP DN)
LDAP_DOMAIN_MAIL=site.edu.ar

# Performs filtering to obtain LDAP groups
# min group_id (group_id>= 500) for ldap search filter
LDAP_GROUP_MIN_VALUE=99
#
# group_id to exclude in ldap search filter
LDAP_GROUP_SKIP_VALUES=[]

# Shows additional information in the search if the registered user
# belongs to any of the indicated groups
GROUPS_EXTRA_INFORMATION_SEARCH=[]
#
# Password length used by default in password change functionality
DEFAULT_PASSWORD_LENGHT=20

# =================================/

## database configuration
DB_NAME=shoal_db
DB_USER=shoal_user
DB_USER_PASSWORD=user_password
DB_OWNER=shoal_owner
DB_OWNER_PASSWORD=owner_password
DB_HOST=db
DB_PORT=5432

# gunicorn
# GUNICORN_TIMEOUT: "3600"
# GUNICORN_LOGLEVEL: "info"
# GUNICORN_BIND: "0.0.0.0:8000"
# GUNICORN_WORKERS: ""
# GUNICORN_THREADS: ""
# GUNICORN_ACCESSLOG: ""
# GUNICORN_ERRORLOG: ""
