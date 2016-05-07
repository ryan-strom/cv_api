"""
WSGI config for cv_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
# import os
# import sys
#
# sys.path.insert(0, '/opt/python/current/app')
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cv_api.settings")
#
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()

import os
import sys
import time
import traceback
import signal

sys.path.insert(0, '/opt/python/current/app')
sys.path.append('/usr/local/lib/python2.7/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'cv_api.settings'

from django.core.wsgi import get_wsgi_application

try:
    application = get_wsgi_application()
    print 'WSGI without exception'
except Exception:
    print 'handling WSGI exception'
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)