from django.conf import settings

def enable_user_password_change (request):
    allow = False
    if hasattr(settings, 'ENABLE_USER_PASSWORD_CHANGE'):
        allow = settings.ENABLE_USER_PASSWORD_CHANGE
    return {'enable_user_password_change': allow}
