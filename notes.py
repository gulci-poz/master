# kontroler jest częścią django, analizuje on urle i przekazuje request
# do odpowiedniej funkcji widoku, funkcja widoku zwraca response,
# django tworzy prawdziwe HTTP response

# django usuwa z urla początkowy slash
# jeśli wzorzec pasuje i nie kończy się slashem, to zapytanie
# zostanie przekierowane do urla ze slashem na końcu
# (serwer zwróci redirect na url z / na końcu)
# jest ustawienie APPEND_SLASH z takim domyślnym zachowaniem
# w momencie zdefiniowania pierwszego urla pochodzącego z naszej aplikacji,
# root url w przeglądarce pokaże nam error 404,
# określamy wtedy widok dla wzorca ^$
# r jest konieczne ze względu na użycie backslasha w wyrażeniach regularnych,
# a nie do escape character
# parametry z urla zawsze będą obiektami Unicode

# timezone na 'Europe/Warsaw'
# instalacja pytz - na potrzeby zapisu czasu UTC w bazie danych
# (jest instalowana z dj 1.11)

# LANGUAGE_CODE = 'en-us'
# lepiej zostawić domyślne en-us i dołączać tłumaczenia

# wyrażenia regularne:
# . dowolny znak
# \d dowolna cyfra
# \w znak ze zbioru [a-zA-Z0-9_]
# \s znak biały
# [A-Z]
# [a-z]
# [A-Za-z] case insensitive
# + jedno lub więcej wystąpień
# [^/]+ jedno lub więcej wystąpień znaku do slasha (bez niego)
# ? zero lub jedno wystąpienie
# * zero lub więcej wystąpień
# {1,3} ilość wystąpień: 1, 2 lub 3

# python manage.py shell
# dostaniemy shell z zaimportowanym django i ustawieniami projektu
# manage.py ustawia zmienną środowiskową DJANGO_SETTINGS_MODULE
# na plik ustawień projektu

# template engine wczytuje surowy szablon
# i kompiluje go do zoptymalizowanej postaci,
# gotowej do wyrenderowania
# (renderowanie uwzględnia podmianę zmiennych i wykonanie tagów)

# jeśli będziemy mieli błąd w szablonie, to dostaniemy TemplateSyntaxError:
# - nieprawidłowe tagi
# - nieprawidłowe argumenty to prawidłowych tagów
# - nieprawidłowe filtry
# - nieprawidłowe argumenty do prawidłowych filtrów
# - nieprawidłowa składnia szablonu
# - niezamknięte tagi (jeśli wymagają zamknięcia)

# obiekt kontekstu daje większą funkcjonalność niż sam słownik

# interaktywny interpreter wyświetli reprezentację stringa (będą znaki \n)
# jeśli chcemy wartość do wydrukowania (nowe linie), to trzeba użyć print

# django ma template backend API, klasy template engine implementują to API

from django.template import Context, Template
from datetime import date

# tworzymy szablon, za pomocą którego później renderujemy wiele kontekstów
# nie tworzymy kontekstu dla każdego szablonu
t = Template('Hello, {{ name }}')
for name in ('John', 'Julie', 'Pat'):
    print(t.render(Context({'name': name})))

# dostęp w szablonie do kluczy, atrybutów, metod, indeksów (np. listy)
# za pomocą kropki

# dostęp do kluczy
person = {'name': 'Sally', 'age': 40}
t = Template('{{ person.name }} is {{ person.age }} years old.')
c = Context({'person': person})
print(t.render(c))

# dostęp do atrybutów
d = date(2017, 6, 2)
t = Template(
    'The month is {{ date|date:"F" }} and the year is {{ date.year }}.')
c = Context({'date': d})
print(t.render(c))


# dostęp do atrybutów dowolnej klasy
class Person(object):
    def __init__(self, first_name, last_name):
        self.first_name, self.last_name = first_name, last_name


p = Person('John', 'Doe')
t = Template('Hello, {{ p.first_name }} {{ p.last_name }}!')
c = Context({'p': p})
print(t.render(c))

# dostęp do metod
# przy wywołaniu nie używamy nawiasów
# możemy wywoływać metody, które nie wymagają argumentów
# logika i przygotowanie danych powinno być wykonane w widoku
t = Template('{{ var }} - {{ var.upper }} - {{ var.isdigit }}')
c = Context({'var': 'hello'})
print(t.render(c))
c = Context({'var': '123'})
print(t.render(c))

# dostęp za pomocą indeksu
# negatywne indeksy są niedozwolone, dostaniemy TemplateSyntaxError
t = Template('Item 2 is {{ items.2 }}.')
c = Context({'items': ['apples', 'bananas', 'carrots']})
print(t.render(c))

# jeśli template engine napotka kropkę, to próbuje w kolejności lookupów:
# - słownik
# - atrybut
# - wywołanie metody
# - dostęp przez indeks listy
# używany jest pierwszy loopup, który działa
# lookupy mogą być zagnieżdżone

person = {'name': 'Sally', 'age': 40}
t = Template('{{ person.name.upper }} is {{ person.age }} years old.')
c = Context({'person': person})
print(t.render(c))


# jeśli metoda wyrzuci wyjątek, to będzie on propagowany

class Person(object):
    def first_name(self):
        raise AssertionError('foo')


t = Template('My name is {{ p.first_name }}.')
p = Person()
print(t.render(Context({'p': p})))


# wyjątek może mieć atrybut silent_variable_failure = True
# wtedy zmienna wyrenderuje się jako wartość
# zmiennej string_if_invalid (domyślnie pusty string)
# ustawiamy 'string_if_invalid': 'ERROR'
# w settings.py, w TEMPLATES, w słowniku OPTIONS
# różne aplikacje korzystają z tego ustawienia,
# więc lepiej zostawić (przynajmniej w produkcji) pusty string


class SilentAssertionError(Exception):
    silent_variable_failure = True


class Person(object):
    def first_name(self):
        raise SilentAssertionError


t = Template('My name is {{ p.first_name }}.')
p = Person()
print(t.render(Context({'p': p})))


# jeśli metoda będzie wywołana z argumentem,
# to lookup przejdzie do rozpoznawania indeksu

# metody mogą mieć efekty uboczne,
# nie powinniśmy takich metod uruchamiać w szablonie

# musimy ustawić na metodzie atrybut delete.alters_data = True
# template engine nie wykona takiej metody
# zostanie użyta wartość z ustawienia string_if_invalid

# metody delete() i seve() modeli django
# mają domyślnie delete.alters_data = True

class Person(object):
    def delete(self):
        print('Removing person account...')

    delete.alters_data = True


p = Person()
t = Template('Side effect: {{ p.delete }}')
t.render(Context({'p': p}))

# jeśli zmienna nie istnieje w kontekście (lookup nie daje rezultatu),
# to używana jest wartość string_if_invalid
# błąd w szablonie nie powoduje unieruchomienia aplikacji

# if - zmienna istnieje & nie jest pusta & nie jest równa False
# trzeba zamykać za pomocą endif, inaczej TemplateSyntaxError

# będziemy mieli kilka \n w stringu
raw_t = """
    {% if today_is_weekend %}
        <p>Welcome to the weekend!</p>
    {% else %}
        <p>Get back to work.</p>
    {% endif %}
"""
t = Template(raw_t)
c = Context({'today_is_weekend': True})
r = t.render(c)
print(r)

# dowolna ilość elif
raw_t = """
    {% if athlete_list %}
        <p>Number of athletes: {{ athlete_list|length }}</p>
    {% elif athlete_in_locker_room_list %}
        <p>Athletes should be out of the locker room soon!</p>
    {% else %}
        <p>No athletes.</p>
    {% endif %}
"""
t = Template(raw_t)
# c = Context({'athlete_list': ['athlete1']})
# c = Context({'athlete_in_locker_room_list': ['athlete1']})
# c = Context()
c = Context({'athlete_list': []})
r = t.render(c)
print(r)

# możemy używać and, or, not
raw_t = """
    {% if athlete_list and coach_list %}
        <p>athletes and coaches</p>
    {% endif %}
"""
t = Template(raw_t)
c = Context({'athlete_list': ['athlete1'], 'coach_list': ['coach1']})
r = t.render(c)
print(r)

raw_t = """
    {% if not athlete_list %}
        <p>no athletes</p>
    {% endif %}
    {% if athlete_list or coach_list %}
        <p>athletes or coaches</p>
    {% endif %}
    {% if not athlete_list or coach_list %}
        <p>no athletes or coaches</p>
    {% endif %}
"""
t = Template(raw_t)
c = Context({'athlete_list': [], 'coach_list': ['coach1']})
r = t.render(c)
print(r)

# and ma pierwszeństwo (precedence) przed or
raw_t = """
    {% if athlete_list and coach_list or cheerleader_list %}
        <p>athletes and coaches, or maybe some cheerleaders</p>
    {% endif %}
"""
t = Template(raw_t)
# c = Context({'athlete_list': ['athlete1'], 'coach_list': ['coach1'],
#              'cheerleader_list': []})
c = Context({'athlete_list': [], 'coach_list': ['coach1'],
             'cheerleader_list': []})
r = t.render(c)
print(r)

# użycie nawiasów w if jest niedozwolone
# można użyć zagnieżdżonych ifów do określenia pierwszeństwa operatorów
# lub wykonać logikę poza widokiem i przekazać rezultat do szablonu

# można wiele razy użyć tego samego operatora,
# kombinacja różnych logicznych operatorów również przechodzi
raw_t = """
    {% if a and b or c and d %}
        <p>allowed</p>
    {% endif %}
"""
t = Template(raw_t)
c = Context({'a': '1', 'b': '2', 'c': '', 'd': ''})
r = t.render(c)
print(r)

# in/not in
raw_t = """
    {% if "bc" in abc %}
        <p>bc in abc</p>
    {% endif %}
    {% if "user3" not in users %}
        <p>no user3</p>
    {% endif %}
"""
t = Template(raw_t)
c = Context({'abc': 'abc', 'users': ['user1', 'user2']})
r = t.render(c)
print(r)

# is/is not
raw_t = """
    {% if var is True %}
        <p>var is True</p>
    {% endif %}
    {% if var is not None %}
        <p>var is not None</p>
    {% endif %}
    {% if name is None %}
        <p>name is None</p>
    {% endif %}
"""
t = Template(raw_t)
c = Context({'var': True, 'name': 'john'})
r = t.render(c)
print(r)

# for
raw_t = """
    <ul>
        {% for user in users %}
            <li>{{ user }}</li>
        {% endfor %}
    </ul>
    <ul>
        {% for user in users reversed %}
            <li>{{ user }}</li>
        {% endfor %}
    </ul>
"""
t = Template(raw_t)
c = Context({'users': ['john', 'norma', 'hal']})
r = t.render(c)
print(r)

# zagnieżdżanie for
raw_t = """
    {% for user in users %}
        <h3>{{ user.name }}</h3>
        <ul>
            {% for lang in user.langs %}
                <li>{{ lang }}</li>
            {% endfor %}
        </ul>
    {% endfor %}
"""
t = Template(raw_t)
c = Context(
    {
        'users': [
            {'name': 'john', 'langs': ['python', 'js']},
            {'name': 'hal', 'langs': ['python', 'c']}
        ]
    }
)
r = t.render(c)
print(r)

# lista list, odpakowujemy wartości z podlist
raw_t = """
    {% for x, y in points %}
        <p>point ({{ x }}, {{ y }})</p>
    {% endfor %}
"""
t = Template(raw_t)
c = Context({'points': [[1, 2], [3, 4], [5, 6]]})
r = t.render(c)
print(r)

# słownik
raw_t = """
    {% for key, value in data.items %}
        <p>{{ key }} - {{ value }}</p>
    {% endfor %}
"""
t = Template(raw_t)
c = Context({'data': {'name': 'john', 'age': 33, 'prof': 'developer'}})
r = t.render(c)
print(r)

# warto sprawdzić, czy lista nie jest pusta
raw_t = """
    {% if data %}
        <ul>
            {% for item in data %}
                <li>{{ item }}</li>
            {% endfor %}
        </ul>
    {% else %}    
        <p>no food</p>
    {% endif %}
"""
t = Template(raw_t)
# c = Context({'data': ['milk', 'toast', 'honey']})
c = Context({'data': []})
r = t.render(c)
print(r)

# identyczne działanie - tag empty
raw_t = """
    <ul>
        {% for item in data %}
            <li>{{ item }}</li>
        {% empty %}
            <li>no food</li>
        {% endfor %}
    </ul>
"""
t = Template(raw_t)
c = Context({'data': []})
r = t.render(c)
print(r)

# nie ma analogów break i continue

# dla każdego segmentu for mamy dostęp do zmiennej forloop i jej atrybutów
# counter - ilość wejść do pętli, indeksowanie od 1
# counter0 - indeksowanie od 0
# revcounter - ilość pozostałych obiegów pętli, od całkowitej liczby elementów
# revcounter0 - realne kroki do końca
# first, last - True, jeśli jesteśmy w pierwszym/ostatnim obiegu pętli
raw_t = """
    <ul>
        {% for item in data %}
            {% if forloop.first %}
                <li class="first">
            {% else %}
                <li>
            {% endif %}
            {{ forloop.revcounter0 }}: {{ item }}</li>
        {% empty %}
            <li>no food</li>
        {% endfor %}
    </ul>
"""
t = Template(raw_t)
c = Context({'data': ['milk', 'toast', 'honey']})
r = t.render(c)
print(r)

# last
raw_t = """
    {% for link in links %}
        {{ link }}{% if not forloop.last %} | {% endif %}
    {% endfor %}
"""
t = Template(raw_t)
c = Context({'links': ['link1', 'link2', 'link3']})
r = t.render(c)
print(r)

# parentloop
raw_t = """
    {% for user in users %}
        <h3>{{ user.name }}</h3>
        <ul>
            {% for lang in user.langs %}
                <li>user {{ forloop.parentloop.counter }}: {{ lang }}</li>
            {% endfor %}
        </ul>
    {% endfor %}
"""
t = Template(raw_t)
c = Context(
    {
        'users': [
            {'name': 'john', 'langs': ['python', 'js']},
            {'name': 'hal', 'langs': ['python', 'c']}
        ]
    }
)
r = t.render(c)
print(r)

# ifequal/ifnotequal - przestarzałe, używamy operatorów == lub !=

# komentarze {# komentarz #} - jednoliniowe
# wydajność parsowania  jest wtedy większa
# wieloliniowy komentarz {# #} zostanie wyrenderowany jako normalny tekst

# właściwy wieloliniowy komentarz,
# może zawierać opcjonalną notkę z wyjaśnieniami:
raw_t = """
    {% comment "optional notes" %}
    {% endcomment %}
"""
# redefinicja bez przyczyny ;)
print(raw_t)

# komentarze nie mogą być zagnieżdżane

# filtry - zmiana wartości zmiennej przed wyświetleniem
raw_t = """
    {{ name|upper }}
    {# chainowanie #}
    {{ names|first|lower }}
    {# argument po dwukropku i w cudzysłowiu #}
    {{ description|truncatewords:"3" }}
    {# dodaje backslash przed \ ' " #} 
    {{ value|addslashes }}
    {# 0 jeśli zmienna nie jest zdefiniowana #}
    {{ names|length }}
    {{ name|length }}
    {{ date|date:"F j, Y" }}
"""
t = Template(raw_t)
c = Context({'name': 'john',
             'names': ['JOE', 'hal', 'pam'],
             'description': 'Very long and versatile description',
             'value': '\\backslash - \'quote - "d-quote',
             'date': date(2017, 6, 2)})
r = t.render(c)
print(r)

# DTL philosophies:
# 1. Separate logic from presentation.
# 2. Discourage redundancy.
# 3. Be decoupled from HTML.
# 4. XML is bad.
# 5. Asume designer competence.
# 6. Treat whitespace obviously (display it).
# 7. Don't invent a programming language.
# 8. Ensure safety and security.
# 9. Extensible.

# dziedziczenie:
# include definiuje wspólne fragmenty
# dziedziczenie definiuje różniące się fragmenty
# silnik widzi extends i wczytuje bazę,
# znalezione bloki próbuje zamienić na bloki z child,
# po tej zamianie następuje renderowanie
# jeśli nie nadpiszemy bloku z bazy, to nie jest on zmieniany (fall-back)
# stanowi on zawartość domyślną
# przy definiowaniu bloku w child robimy override bloku z bazy
# dodawanie do bloku za pomocą {{ block.super }}, silnik wstawia wyrenderowany
# blok z bazy i dopisuje do niego część z child
# mamy osobny proces renderowania - jak z include (notatki z greeting.html)
# dziedziczenie nie ma wpływu na kontekst
# kontekst jest pamiętany również w inkludowanym szablonie
# nie możemy duplikować nazw bloków
# 3-level approach: baza - szablon sekcji - szablon typu strony
# extends musi być pierwszym tagiem
# argumentem do extends może być zmienna
# (dynamiczne ładowanie szablonu w runtime)
# mamy szukanie po APP_DIRS i DIRS
