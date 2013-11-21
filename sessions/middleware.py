import datetime

from django.http import HttpResponseRedirect
from django.conf import settings

from accounts.utils import cosign_logout


class SessionIdleTimeout:
    """Middleware class to timeout a session after a specified time period.
    """

    def process_request(self, request):
        # Timeout is done only for authenticated logged in users.
        if request.user.is_authenticated():
            current_datetime = datetime.datetime.now()
            # Timeout if idle time period is exceeded.
            if request.session.has_key('last_activity') and \
                            (current_datetime - request.session['last_activity']).seconds > \
                            settings.SESSION_IDLE_TIMEOUT:
                cosign_logout(request)
                # Note, with redirect, the inbound request seems to not subsequently correspond
                # to referer, but we assume that what the user actually wants to do is
                # continue on to location that was interrupted by timing out
                response = HttpResponseRedirect(settings.SESSION_TIMED_OUT_URL)
                response.set_cookie('previous', value=request.path)
                return response
            # Set last activity time in current session.
            else:
                request.session['last_activity'] = current_datetime
        return None

