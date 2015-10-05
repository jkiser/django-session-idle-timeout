from django.apps import AppConfig

# this is necessary owing to 1.7 changes that cause errors related
# to app name uniqueness.

class DjangoSessionIdleTimeoutConfig(AppConfig):
    name = 'sessions'
    label = 'idletimeout.sessions'
    verbose_name = 'Django Session Idle Timeout'
