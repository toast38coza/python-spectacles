from django.conf import settings
import uuid


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
