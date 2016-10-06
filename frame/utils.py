import json
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.module_loading import import_string
import re

DIV_PATTERN = '<div id="language">.*?</div>'
A_PATTERN = '(<a.*?</a>).*(<a.*?</a>)'
LANG_PATTERN = '<a.*?>([a-z]{2})</a>'


def get_current_language(frame_html):
    div_elem = re.search(DIV_PATTERN, frame_html, re.DOTALL)
    if not div_elem:
        return None
    div_elem = div_elem.group()
    a_elems = re.search(A_PATTERN, div_elem, re.DOTALL).groups()
    for a_elem in a_elems:
        if 'current' in a_elem:
            language = re.search(LANG_PATTERN, a_elem, re.DOTALL).groups()
            if language:
                return language[0]
    return None


def get_forwarded_cookies(request):
    forwarded_cookies = {}
    for name in getattr(settings, 'FRAME_COOKIES', []):
        if name in request.COOKIES:
            forwarded_cookies[name] = request.COOKIES[name]
    return forwarded_cookies


def get_objects_from_last_seen_count(request):
    """ View returning a json with the count of objects from last seen.
    """
    if not request.user.is_authenticated():
        raise PermissionDenied()

    models = getattr(settings, 'FRAME_SEEN_MODELS', None)
    if not models:
        raise ValueError('No models were set')

    from frame.models import Seen

    try:
        seen = request.user.seen
        seen = seen.seen
    except Seen.DoesNotExist:
        seen = None

    count = 0
    for model_name, field in models:
        model = import_string(model_name)
        if seen:
            count += model.objects.filter(**{'%s__gte' % field: seen}).count()
        else:
            count += model.objects.count()

    data = {
        'count': count,
        'seen': seen and seen.strftime('%Y-%m-%d %H:%M:%s'),
        'user': request.user.username,
    }
    return HttpResponse(json.dumps(data),
                        content_type='application/json')
