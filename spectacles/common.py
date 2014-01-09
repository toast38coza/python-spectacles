from django.conf import settings
import uuid
from django.contrib import auth

DEFAULT_WAIT_TIME = 5

def get_absolute_url(path):

    if path.startswith("/"):
        path = path[1:]

    baseurl = settings.TEST_DOMAIN 

    if baseurl[-1] != "/":
        baseurl = "{0}/".format(baseurl)
            
    return "{0}{1}" . format (baseurl, path)


def _short_password():
    return str(uuid.uuid4()).split("-")[0]

def _create_user(username_template):

    username = username_template . format( _short_password() )
    return auth.get_user_model().objects.create(username=username, password="test")