from datetime import datetime, timedelta

from django.http import Http404, HttpResponse
from django.template import Context, Template


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


def order_notice(request):
    t = Template(
        """
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
    )
    c = Context({
        'person_name': 'John Doe',
        'company': 'gooseberry',
        'ship_date': datetime.now() + timedelta(72),
        'item_list': ['scissors', 'paper', 'rock'],
        'ordered_warranty': True,
    })
    rt = t.render(c)
    return HttpResponse(rt)
