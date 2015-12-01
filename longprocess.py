import os
import sys
from django.conf import settings
from django.http import JsonResponse
from django.conf.urls import url
from django.http import HttpResponse
from multiprocessing import Process, Value
from time import sleep

progress_timer = Value('d', 0.0)


def process():
    t = 0
    while t < 10:
        sleep(1)
        t += 1
        progress_timer.value = t
        yield t


def expensive_process():
    for i in process():
        print i


p = Process(target=expensive_process)


def index(request):
    with open('index.html', 'r') as f:
        template = f.read()
    return HttpResponse(template)


def status(request):
    return JsonResponse({'started': p.is_alive()})


def start_process(request):
    try:
        p.start()
        started = True
    except AssertionError:
        started = False
    data = {'started': started}
    return JsonResponse(data)


def stop_process(request):
    p.terminate()
    p.join()
    return JsonResponse({'started': False})


def get_process_progress(request):
    return JsonResponse({'progress': progress_timer.value})


urlpatterns = (
    url(r'^$', index),
    url(r'^start', start_process),
    url(r'^report', get_process_progress),
    url(r'^status', status),
    url(r'^stop', stop_process),
)

if __name__ == "__main__":
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
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
