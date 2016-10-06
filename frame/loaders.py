from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.loaders.base import Loader as BaseLoader
from frame.middleware import get_current_request
from frame.utils import get_forwarded_cookies
import requests


class Loader(BaseLoader):
    is_usable = True

    def _process_resp(self, html):
        substitutions = [
            ("{%", "{% templatetag openblock %}"),
            ("%}", "{% templatetag closeblock %}"),
            ("{{", "{% templatetag openvariable %}"),
            ("}}", "{% templatetag closevariable %}"),
            ("<!-- block_messages -->",
             "{% block action_buttons %}{% endblock %}"
             "{% block messages %}{% endblock %}"),
            ("<!-- block_content -->",
             "{% block zope_content %}{% endblock %}"),
            ("<!-- block_head -->",
             "{% block head %}{% endblock %}"),
            ("src=\"misc_/", "src=\"/misc_/"),
        ]

        if getattr(settings, 'FRAME_EXTRA_SUBSTITUTIONS', None):
            substitutions += settings.FRAME_EXTRA_SUBSTITUTIONS

        html = html.strip()
        for sub_a, sub_b in substitutions:
            html = html.replace(sub_a, sub_b)
        return html

    def load_template_source(self, template_name, template_dirs=None):
        request = get_current_request()

        if (request and getattr(settings, 'FRAME_URL', None)
                and template_name == 'frame.html'):

            forwarded_cookies = get_forwarded_cookies(request)

            resp = requests.get(settings.FRAME_URL, cookies=forwarded_cookies)
            resp_json = resp.json()
            if (resp.status_code == 200 and resp_json):
                frame_response = self._process_resp(resp_json['frame_html'])
                return frame_response, template_name

        raise TemplateDoesNotExist(template_name)

    load_template_source.is_usable = True
