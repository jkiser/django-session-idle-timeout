import datetime

from django.utils.translation import ugettext as _
from django.contrib import messages
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.contrib.sites.models import get_current_site
from django.conf import settings

from accounts.utils import cosign_logout


class SessionIdleTimeout:
    """Middleware class to timeout a session after a specified time period.
    """
    def __init__(self):
        self.requested_path = ""

    def process_request(self, request):
        # Timeout is done only for authenticated logged in users.
        if request.user.is_authenticated():
            current_datetime = datetime.datetime.now()
            # Timeout if idle time period is exceeded.
            if request.session.has_key('last_activity') and \
                (current_datetime - request.session['last_activity']).seconds > \
                settings.SESSION_IDLE_TIMEOUT:
                cosign_logout(request)
                messages.add_message(request, messages.ERROR, 'Your session has been timed out.')
                self.requested_path = request.path
                return redirect(settings.SESSION_TIMED_OUT_URL)
            # Set last activity time in current session.
            else:
                request.session['last_activity'] = current_datetime
        return None

    def process_template_response(self, request, response):
        if request.path == settings.SESSION_TIMED_OUT_URL:
            current_site = get_current_site(request)
            current_app = "accounts"
            template_name = "registration/timed_out.html"
            context = {
                "site": current_site,
                "site_name": current_site.name,
                "page_title": _("Session timeout"),
                "previous_url": self.requested_path,
                }
            return TemplateResponse(request, template_name, context, current_app=current_app)
        return response

