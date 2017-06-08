from datetime import datetime, timedelta

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.template import Context, Template, RequestContext
from django.template.loader import get_template


def hello(request):
    return HttpResponse(f'hello {request.method}')


def current_datetime(request):
    now = datetime.now()
    html = f'<html><body>It is now {now}.</body></html>'
    return HttpResponse(html)


def hours_ahead(request, offset=1):
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


def order_notice(request):
    t_raw = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Ordering notice</title>
        </head>
        <body>
        <h1>Ordering notice</h1>
        <p>Dear <strong>{{ person_name }}</strong>,</p>
        <p>Thanks for placing an order from <em>{{ company }}</em>.
            It's scheduled to ship on {{ ship_date|date:"F j, Y" }}.</p>
        <p>Here are the items you've ordered:</p>
        <ul>
            {% for item in item_list %}
                <li>{{ item }}</li>
            {% endfor %}
        </ul>
        {% if ordered_warranty %}
            <p>Your warranty information
                will be included in the packaging.</p>
        {% else %}
            <p>You didn't order a warranty, so you're on your own
                when the products inevitably stop working.</p>
        {% endif %}
        <p>Sincerely,<br><em>{{ company }}</em></p>
        </body>
        </html>
    """

    t = Template(t_raw)

    c = Context({
        'person_name': 'John Doe',
        'company': 'gooseberry',
        'ship_date': datetime.now() + timedelta(72),
        'item_list': ['scissors', 'paper', 'rock'],
        'ordered_warranty': True,
    })

    t_rendered = t.render(c)

    return HttpResponse(t_rendered)


def current_datetime_get_template(request):
    now = datetime.now()

    # dostajemy skompilowany obiekt Template
    # jest to obiekt django.template.backends.django.Template
    # (zależny od backendu)
    # jest to inny obiekt niż django.template.Template
    # tutaj metoda render przyjmuje słownik, a nie Context
    # szukanie po APP_DIRS i DIRS (w porządku)
    # nie znalezienie szablonu - TemplateDoesNotExist
    t = get_template('current_datetime_new.html')

    html = t.render({'current_date': now})
    return HttpResponse(html)


def current_datetime_render_shortcut(request):
    now = datetime.now()
    # mamy wszystkie kroki: template, context (opcjonalny), render
    # i http response, który jest zwracany przez render()
    # render() to wrapper na get_template()
    return render(request, 'current_datetime_new.html', {'current_date': now})


def greeting(request):
    sample_html = '<h2>hello</h2>'
    return render(request, 'greeting.html',
                  {'included_template': 'includes/nav.html',
                   'current_section': 'greeting',
                   'sample_html': sample_html})


def utilities_time(request):
    now = datetime.now()
    return render(request, 'utilities/time.html',
                  {'current_section': 'time', 'current_date': now})


def utilities_time_ahead(request, offset=1):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()

    time_ahead = datetime.now() + timedelta(hours=offset)
    return render(request, 'utilities/time_ahead.html',
                  {'current_section': 'time ahead', 'time_ahead': time_ahead})


def utilities_request(request):
    # generator
    req_iter = request.GET.items()

    # GET i POST to obiekty dictionary-like

    return render(request, 'utilities/request_object.html',
                  {
                      'current_section': 'request_object',
                      'rmethod': request.method,
                      'rgetlen': len(request.GET),
                      'rget': request.GET,
                      # /utilities/request/?bla=bla&name=user
                      'rgetitems': next(req_iter),
                      'rgetitems2': next(req_iter),
                      'rgetbla': request.GET.get('bla'),
                      'rgetbladict': request.GET['bla'],
                      'rpath': request.path,

                      # przekazujemy metody
                      'rhost': request.get_host,
                      'rfull': request.get_full_path,
                      'rsecure': request.is_secure,

                      'rmeta': request.META,
                      'rmetakeys': request.META.keys(),

                      'rreferer': request.META.get('HTTP_REFERER', 'unknown'),
                      'ragent': request.META.get('HTTP_USER_AGENT', 'unknown'),
                      'raddr': request.META.get('REMOTE_ADDR', 'unknown'),
                  })


def utilities_display_meta(request):
    meta_values = sorted(request.META.items())

    return render(request, 'utilities/request_meta.html',
                  {'current_section': 'request_meta',
                   'meta_values': meta_values})


def debug(request):
    return HttpResponse('<html><body><p>Debug view</p></body></html>')


def handler404(request):
    return HttpResponseNotFound('<html><body><p>Ooops... 404</p></body></html>')


def testing(request, num, meta):
    url_resolved = reverse('testing', args=(0,))
    return HttpResponse(f'{num} - {meta} - {url_resolved}')


def custom_cp(request):
    return {
        'app': 'My App',
        'ip_address': request.META['REMOTE_ADDR']
    }


def cp(request):
    # jeśli chcemy do render() przekazać obiekt RequestContext,
    # to nie możemy użyć szablonu wygenerowanego przez get_template(),
    # ponieważ render() na obiekcie django.template.backends.django.Template
    # przyjmuje słownik
    # t = get_template('some_template.html')

    t = Template('{{ app }} - {{ user }} - {{ ip_address }}')
    # możemy użyć nazwanego argumentu processors
    # ma to być lista lub krotka
    c = RequestContext(request, {'current_section': 'cp'}, [custom_cp])
    return HttpResponse(t.render(c))


def cpshort(request):
    # do render() z django.shortcuts możemy przekazać kontekst
    # w postaci słownika, wartość w słowniku może być callable
    # nie możemy przekazać RequestContext
    # w przypadku cp musimy podać argument, więc sami robimy wywołanie
    # w przypadku np. datetime.now widok sam wywoła funkcję przed renderowaniem
    return render(request, 'cpshort.html',
                  {'current_section': 'cpshort', 'cp': custom_cp(request)})


def cpglobal(request):
    return render(request, 'cpglobal.html',
                  {'current_section': 'cpglobal'})
