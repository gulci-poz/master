from datetime import datetime, timedelta

from django.http import Http404, HttpResponse


def hello(request):
    return HttpResponse(f'hello {request.method}')


def current_datetime(request):
    now = datetime.now()
    html = f'<html><body>It is now {now}.</body></html>'
    return HttpResponse(html)


def hours_ahead(request, offset):
    # loose coupling - urlconf sprawdza wzorzec, ale nie robimy założenia,
    # że zawsze tak będzie, widok tak naprawdę nie wie co dostaje
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()

    dt = datetime.now() + timedelta(hours=offset)
    html = f'<html><body>In {offset} hours, it will be {dt}.</body></html>'
    # debugowanie ala print
    # assert False
    return HttpResponse(html)
