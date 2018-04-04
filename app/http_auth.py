import base64
from django.contrib.auth import authenticate
import logging
def basic_http_authentication(request):
    if not 'HTTP_AUTHORIZATION' in request.META:
        return None
    
    auth = request.META['HTTP_AUTHORIZATION'].split()
    user = None
    if len(auth) == 2:
        if auth[0].lower() == "basic":
            uname, passwd = base64.b64decode(auth[1]).split(':')
            logging.error("{} {}".format(uname, passwd))
            user = authenticate(username=uname, password=passwd)
    return user


