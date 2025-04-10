from threading import local
import requests
import logging

from frame.utils import get_current_language, get_forwarded_cookies
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

User = get_user_model()

_thread_locals = local()

logger = logging.getLogger('eea.frame')


def get_current_request():
    return getattr(_thread_locals, 'request', None)


class RequestMiddleware:
    """
    Middleware that gets various objects from the
    request object and saves them in thread local storage.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        response = self.get_response(request)
        return response


class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def _fetch_data(self):
        request = get_current_request()
        forwarded_cookies = get_forwarded_cookies(request)
        verify = getattr(settings, 'FRAME_VERIFY_SSL', None)
        try:
            resp = requests.get(settings.FRAME_URL, cookies=forwarded_cookies,
                                verify=verify)
            data = resp.json()
        except Exception as e:
            logging.exception(e)
            data = {}
        else:
            data.setdefault('frame_html', '')
        return data

    def process_request(self, request):
        if getattr(settings, 'FRAME_URL', None):
            resp_json = self._fetch_data()
            if resp_json:
                request.user_id = resp_json['user_id']
                request.user_roles = resp_json['user_roles']
                request.user_groups = resp_json['groups']
                request.language = (
                    get_current_language(resp_json['frame_html']) or
                    getattr(settings, 'DEFAULT_LANGUAGE', None)
                )
                if request.user_id:
                    try:
                        request.user = User.objects.get(
                            username=request.user_id)
                    except User.DoesNotExist:
                        request.user = AnonymousUser()
                    request.META['REMOTE_USER'] = {
                        'user_id': request.user_id,
                        'user_roles': request.user_roles,
                        'user_groups': request.user_groups,
                    }
                else:
                    request.user = AnonymousUser()
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

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        return response


class SeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        from frame.models import Seen

        seen_exclude = getattr(settings, 'FRAME_SEEN_EXCLUDE', [])
        if request.path_info in seen_exclude:
            return

        if not request.user.is_authenticated():
            return

        seen, new = Seen.objects.get_or_create(user=request.user)
        seen.save()

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        return response


# keep this for compatibility
from frame.loaders import Loader
