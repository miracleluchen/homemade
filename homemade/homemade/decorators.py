from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import PermissionDenied
from django.utils.timezone import now, localtime
import logging
import json

log = logging.getLogger('main')

def secure_required(func):
    """
    Decorator makes sure URL is accessed over https.
    Use with `SecureRequiredMiddleware` to ensure only decorated urls are
    accessed via https
    """
    def wrap(request, *args, **kwargs):
        request.secure_required = True
        if not request.is_secure():
            if getattr(settings, 'HTTPS_SUPPORT', False):
                request_url = request.build_absolute_uri(request.get_full_path())
                secure_url = request_url.replace('http://', 'https://')
                return  HttpResponseRedirect(secure_url)
        return func(request, *args, **kwargs)
    return wrap

def logger_for_view(func, view_name):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated():
            user = request.user.email
        else:
            if settings.DEVELOPMENT:
                user = settings.DEBUG_USER
            else:
                raise PermissionDenied()
        log.info("access view %s, user: %s, time:%s" % (view_name, user, localtime(now())))
        return func(request, *args, **kwargs)
    return wrap
