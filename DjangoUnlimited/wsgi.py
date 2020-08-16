"""
WSGI config for DjangoUnlimited project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# add the hellodjango project path into the sys.path
sys.path.append('/home/ubuntu/django/InnovateSolutions/DjangoUnlimited')

# add the virtualenv site-packages path to the sys.path
sys.path.append('/home/ubuntu/django/myprojectenv/bin/lib/python2.7')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoUnlimited.settings')

application = get_wsgi_application()
