from django.conf import settings
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
