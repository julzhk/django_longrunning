import os
import sys
from django.conf import settings

from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse


# application = get_wsgi_application()

def index(request):
    return HttpResponse('Hello World')

urlpatterns = (
    url(r'^$', index),
)

if __name__ == "__main__":
    settings.configure(
        DEBUG=True,
        DATABASES = {
        'default': {
            'ENGINE':'django.db.backends.sqlite3',
            'NAME': 'None',
            }
        },
        SECRET_KEY=os.environ.get('SECRET_KEY', '2342tfdgfdgdfgDSFDSFsdgsdf2234252'),
        ROOT_URLCONF=__name__,
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ),
    )

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)