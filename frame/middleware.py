from threading import local
import requests

from frame.utils import get_current_language, get_forwarded_cookies
from django.conf import settings


_thread_locals = local()


def get_current_request():
    return getattr(_thread_locals, 'request', None)


class RequestMiddleware(object):
    """
    Middleware that gets various objects from the
    request object and saves them in thread local storage.
    """

    def process_request(self, request):
        _thread_locals.request = request


class UserMiddleware(object):
    def process_request(self, request):
        request = get_current_request()
        if getattr(settings, 'FRAME_URL', None):
            forwarded_cookies = get_forwarded_cookies(request)
            verify = getattr(settings, 'FRAME_VERIFY_SSL', None)
            resp = requests.get(settings.FRAME_URL, cookies=forwarded_cookies,
                                verify=verify)
            resp_json = resp.json()
            if (resp.status_code == 200 and resp_json):
                request.user_id = resp_json['user_id']
                request.user_roles = resp_json['user_roles']
                request.user_groups = resp_json['groups']
                request.language = (
                    get_current_language(resp_json['frame_html']) or
                    getattr(settings, 'DEFAULT_LANGUAGE', None)
                )
                if request.user_id:
                    request.META['REMOTE_USER'] = {
                        'user_id': request.user_id,
                        'user_roles': request.user_roles,
                        'user_groups': request.user_groups,
                    }
        else:
            request.user_id = getattr(settings, 'USER_ID', None)
            request.user_roles = getattr(settings, 'USER_ROLES', None)
            request.user_groups = getattr(settings, 'USER_GROUPS', None)
            request.language = getattr(settings, 'DEFAULT_LANGUAGE', None)

        if not getattr(request, 'user_id', None):
            request.user_id = None
        if not getattr(request, 'user_roles', None):
            request.user_roles = []
        if not getattr(request, 'user_groups', None):
            request.user_groups = []


class SeenMiddleware(object):
    def process_request(self, request):
        from frame.models import Seen

        seen_exclude = getattr(settings, 'FRAME_SEEN_EXCLUDE', [])
        if request.path_info in seen_exclude:
            return

        if not request.user.is_authenticated():
            return

        seen, new = Seen.objects.get_or_create(user=request.user)
        seen.save()


# keep this for compatibility
from frame.loaders import Loader
