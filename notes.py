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
# DEBUG musi być False


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

# modele mudzą istniejć wewnątrz aplikacji django
# model to data layout - odpowiednik instrukcji SQL CREATE TABLE
# model daje wiecej możliwości niż czysty SQL (np. dodanie zachowania)
# introspekcja bazy w runtime dawałaby zbyt duży narzut (overhead)
# dzięki modelowi możemy wersjonować layout danych
# synchronizacja modelu i bazy danych - migracje
# w django można wygenerować model poprzez introspekcję bazy danych
# jedna klasa (model) to jedna tabela bazy danych
# wyjątkiem jest relacja m2m
# nie dostajemy kolumny, django tworzy dodatkową tabelę join dla m2m
# domyślnie django tworzy pole iteger id, które jest auto-increment pk
# jest wymagane, żeby każdy model django miał jednokolumnowy pk
# walidacja modelu:
# -> python manage.py check
# jest to check framework django
# zestaw statycznych checków do walidacji projektu django
# wyłapuje problemy z modelami
# informujemy, że zrobiliśmy zmiany w modelu danych:
# -> python manage.py makemigrations books
# wyświetlamy kod SQL, który zostanie wykonany przez daną migrację
# -> python manage.py sqlmigrate books 0001
# domyślnie nazwa tabeli to nazwa aplikacji + nazwa modelu (można to zmienić)
# django generuje pk - pole id (można to zmienić)
# django dodaje _id do nazwy klucza obcego (można to zmienić)
# relacja klucza obcego jest tworzona explicite przez instrukcję REFERENCES
# aktualizacja schematu bazy danych na podstawie osatniego pliku migracji
# (wykonanie kodu SQL z sqlmigrate)
# -> python manage.py migrate

# -> python manage.py shell

from books.models import Publisher

# jeśli chcemy od razu zapisać obiekt w bazie, to używamy
# Publisher.objects.create()

p1 = Publisher(name='Apress', address='2855 Telegraph Avenue', city='Berkeley',
               state_province='CA', country='U.S.A.',
               website='http://www.apress.com/')
# INSERT INTO
p1.save()
p2 = Publisher(name="O'Reilly", address='10 Fawcett St.', city='Cambridge',
               state_province='MA', country='U.S.A.',
               website='http://www.oreilly.com/')
p2.save()

# SELECT
# django nie robi SELECT * tylko explicite podaje każde pole
# managery zajmują się wszystkimi operacjami na danych na poziomie tabeli
publisher_list = Publisher.objects.all()
publisher_list

# możemy odczytać id
publisher_list[0].id
# możemy odczytać pk
publisher_list[0].pk

# __str__ dodaje zachowanie do modelu
# __str__ musi zwracać stringa, w przeciwnym razie python wyrzuci TypeError

p = Publisher(name='GNW Independent Publishing', address='123 Some Street',
              city='Hamilton', state_province='NSW', country='AUSTRALIA',
              website='http://djangobook.com/')
p.save()

p.name = 'GNW Independent Publishing'
# UPDATE - kolejne wywołania save robią UPDATE
# będzie update wszystkich pól (możemy mieć race condition)
p.save()

# WHERE
Publisher.objects.filter(name='Apress')
Publisher.objects.filter(country='U.S.A.', state_province='CA')
# LIKE
Publisher.objects.filter(name__contains='press')

# wyciąganie pojedynczego obiektu, a nie QuerySet
# wyjątek w przypadku wielu obiektów (MultipleObjectsReturned)
# wyjątek w przypadku braku obiektu (DoesNotExist)
# Publisher.DoesNotExist - jest to atrybut klasy modelu
# trzeba używać try
try:
    apress = Publisher.objects.get(name='Apress')
except Publisher.DoesNotExist:
    print('no data')
else:
    print(f'data ok: {apress}')

# domyślne sortowanie można określić w modelu, w klasie meta (lista ordering)
# nadal możemy explicite określić sortowanie przy wyciąganiu danych
Publisher.objects.order_by('-name', 'state_province')

# chaining lookupów
Publisher.objects.filter(country='U.S.A.').order_by('-name')

# nie jest obsługiwane indeksowanie ujemne (AssertionError)
# slicing; SQL: LIMIT 1
Publisher.objects.order_by('name')[0]
# slicing; SQL: OFFSET 0 LIMIT 1
Publisher.objects.order_by('name')[0:2]

# update tylko jednego pola (z save() jest update wszystkich pól, możemy mieć
# race condition, inny proces może zmieniać inne kolumny)
# update() działa na QuerySet, musimy użyć filter()
# zwraca integer - liczbę zmienionych rekordów
Publisher.objects.filter(id=1).update(name='Apress Publishing')
Publisher.objects.filter(country='U.S.A.').update(country='USA')

for pub in Publisher.objects.all():
    print(f'{pub.name}, {pub.country}')

# usuwanie
# zwraca krotkę z liczbą rekordów, które będą usunięte
# oraz słownikiem zawierającym model (key)
# i liczbę rekordów usuniętych z tego modelu (value)
# (dla każdego dotkniętego modelu)
# można też usunąć kilka rekordów - delete() na QuerySet (rezultat filter())
p = Publisher.objects.get(name='O\'Reilly')
p.delete()
Publisher.objects.filter(country='USA').delete()

# dostaniemy AttributeError - obiekt managera nie ma atrybutu delete
Publisher.objects.delete()
# jeśli chcemy usunąć wszystko musimy explicite użyć all() na managerze
# jeśli usuwamy podzbiór, to all() nie jest konieczne, wystarczy np. filter()
Publisher.objects.all().delete()


# django na starcie uruchamia admin.autodiscover()
# ta funkcja iteruje po INSTALLED_APPS
# i uruchamia napotkane pliki admin.py
# django.contrib.auth ma swój plik admin.py (widzimy użytkowników i grupy)
# nie zmieniamy widoków, szablonów i urli bezpośrednio w instalacji django

# informacja blank=True dotyczy formularza w django admin, a nie bazy
# nie trzeba robić migracji
# django wszystkie kolumny definiuje jako NOT NULL
# wartość NULL w SQL umożliwia wstawienie pustego stringa
# data, czas, liczby - nie akceptują pustego stringa,
# (DateField, TimeField, DateTimeField, IntegerField, DecimalField, FloatField)
# wtedy trzeba określić w modelu null=True
# w przypadku takich wartości trzeba podać zarówno null jak i blank
# nie kapitalizujemy verbose_name, chyba, że zawsze ma być z wielkiej litery

# sortowanie w klasach ModelAdmin używa do sortowania
# tylko pierwszego pola z podanej listy
# jeśli nie podamy ordering w ModelAdmin, to brane jest ordering z modelu
# formularz edycji
# fields określa kolejność wyświetlania pól na formularzu edycji
# domyślnie brana jest kolejność z modelu
# jeśli nie podamy jakiegoś pola, to będzie ono wykluczone z wyświetlania
# trzeba się upewnić, że takie pole ma null=True,
# ponieważ przy dodawaniu rekordu django będzie ustawiać null
# filter_horizontal - dla pola m2m (nie działa dla foreign key),
# poziome listy z dostępnymi i dodanymi wartościami
# (zamiast multiple-select boksów)
# filter_horizontal można używać dla wielu pól
# mamy też filter_vertical
# dla foreign key mamy raw_id_fields (działa też z m2m),
# django nie ładuje wtedy wszystkich wartości przy rozwijaniu select boksa
# w raw_id_fields mamy wartości id po przecinku

# flagi użytkownika - active, staff (logowanie do interfejsu admina),
# superuser (permissions są ignorowane)
# możmy zarządzać dostępem tym samym kontem do innych aplikacji,
# flaga staff rozróżnia publicznych użytkowników
# (mogą być tak naprawdę "adminami" innych aplikacji) i adminów (mają włączoną)
# każdy obiekt ma 3 uprawnienia do ustawienia: create, edit, delete
# uprawnienia są na model, a nie na instancję (da się to zrobić)
# implicite superuser - gdy nadamy użytkownikowi uprawnienie do edycji uprawnień

# aplikacja admin jest dla użytkowników nietechnicznych,
# którzy będą wprowadzali dane
# model jest tworzony w uzgodnieniu z developerem,
# na podstawie wprowadzonych danych developer tworzy view i template,
# dla strony, która będzie dostępna na zewnątrz
# admin może też służyć do:
# - testowania/inspekcji modelu - wprowadzanie przykładowych danych,
# żeby sprawdzić, czy model zachowuje się tak jak planowaliśmy
# - wygodne zarządzanie i edycja danych (np. dane wprowadzone przez użytkownika)
# - budowanie prostej aplikacji do zarządzania danymi
# aplikacja admin nie jest w zamierzeniu publicznym interfejsem do danych
# jest to aplikacja do administracji i edycji strony
# przez uprawnionych użytkowników

# formularze
# f.as_table() - domyślnie - nie uwzględnia <table></table>
# f.as_ul() - nie uwzględnia <ul></ul>
# f.as_p()
# powyższe outputy nie uwzględniają <form></form>
# można wyświetlić html dla konkretnego pola
# dostaniemy same pole input (bez label)
# f['subject']
# jeśli przekażemy dane, to otrzymamy powiązany (bound) formularz
# (bound jest True jeśli podamy choć jeden dowolny atrybut, może to być '')
# f = ContactForm({'subject': 'cmt', 'email': 'sth@sth.com', 'message': 'msg'})
# f.is_bound
# formularz (również pusty) można walidować
# f.is_valid()
# mamy dostęp do błędów poszczególnych pól
# (lista errors jest pusta dla wszystkich pól jeśli formularz nie jest bound)
# f = ContactForm({'subject': 'cmt', 'message': ''})
# f['message'].errors
# domyślnie puste errors dla maila z pustym stringiem
# formularz jest poprawny z pustym stringiem w mailu
# jeśli formularz jest bound to mamy słownik errors
# f.errors
# formularz, który jest valid ma dostępny atrybut cleaned_data
# f.cleaned_data
# jest to słownik z przesłanymi danymi,
# wartości są przekonwertowane do typów pythonowych

# backendy emailowe
# filebased - wysyłanie maila do pliku w lokalnym systemie plików
# locmem - zapisywanie maila do atrybutu w pamięci
# dummy - wysyłanie maila do dummy backend
# w przypadku HTML5 przeglądarki mogą walidować formularze
# dajemy novalidate, chcemy, żeby django robiło walidację
# fields - logika walidacji
# widgets - logika prezentacji
# z danymi initial formularz nie jest bound, nie będzie błędów

# walidacja komentarzy
# jeśli będziemy chcieli ponownie użyć zdefiniowanej zasady,
# to warto pomyśleć o stworzeniu nowego typu pola
# do jednorazowego użytku możemy związać walidację z klasą Form
# używamy metody clean_message() w klasie ContactForm
# framework formularzy django szuka metod o nazwie rozpoczynającej się
# od clean_ z dodatkiem nazwy pola, np. clean_message
# takie metody są uruchamiane w trakcie walidacji, po uruchomieniu
# głównej ligiki walidacyjnej dla danego pola (tutaj walidacja pola CharField)
# dane z pola już są częściowo przetworzone, więc używany self.cleaned_data
# domyślny walidator sprawdza istnienie i non-empty
# musimy pamiętać o return z oczyszczoną wartością,
# inaczej będzie zwrócone None i stracimy dane

# możemy za pomocą szablonu sami zbudować formularz
# mamy dostęp do pól formularza za pomocą {{ form.fieldname }}
# oraz do powiązanych błędów {{ form.fieldname.errors }}
# listę form.fieldname.errors możemy traktować jako boolean lub iterować po niej

# urlconfs
# wyrażenia z urlconf są sprawdzane po kolei, dlatego specjalne przypadki
# warto zamieszczać przed genrycznymi dopasowaniami
# wybierane jest pierwsze dopasowanie

# nazywamy grupę za pomocą (?P<name>pattern),
# możemy przekazywać nienazwany argument (pattern)

# algorytm:
# jeśli istnieją nazwane argumenty, to zostaną one użyte,
# nienazwane argumenty zostaną zignorowane
# jeśli nie ma nazwanych argumentów,
# to nienazwane zostaną przekazane jako pozycyjne
# w obu przypadkach będą przekazane dodatkowe argumenty keyword

# dopasowanie jest do urla - bez domeny i parametrów metody
# urlconf nie bierze pod uwagę metody, żądania za pomocą dowolnej metody
# będą routowane do tej samej funkcji dla danego urla

# bez względu na typ znaków w dopasowaniu (np. integery),
# argument zostanie przekazany do widoku jako string

# w widoku możemy określić domyślną wartość nazwanego argumentu
# jeśli dwa dopasowania są obsługiwane tą samą funkcję widoku
# pierwsze może nie uwzględniać żadnej wartości,
# wtedy przydaje się wartość domyślna

# każde wyrażenie regularne z urlconf jest kompilowane przy pierwszym dostępie

# w razie niedopasowania lub wyjątku istnieją specjalne widoki określone
# przez zmienne: handler404, handler500, handler403, handler400
# wartości muszą być nadane w root urlconf
# muszą to być callable lub string reprezentujący full import path do widoku
# widok musi zwracać HttpResponseNotFound
# niestandardowa obsługa błędów działa tylko z DEBUG=False

# inkludowane urle mogą pochodzić z dodatkowej listy w tym samym pliku
# w include() podajemy nazwę zmiennej zawierającej tablicę
# dodatkowa tablica zawiera urle relatywne do nadrzędnego
# możemy też ustalić wspólny prefix i za pomocą include pogrupować sufiksy
# (inline lub w zmiennej)
# inkludowany urlconf ma dostęp do wszystkich przechwyconych parametrów

# możemy przekazać trzeci argument do widoku - słownik z metadanymi
# w razie takiej samej nazwy jak przechwycony argument
# argument ze słownika ma pierwszeństwo

# opcjonalny słownik można przekazać również w include
# będzie on przekazany do każdej linii url inkludowanego pliku (listy),
# a zatem do widoku, który to dopasowanie obsługuje
# (ponieważ ten słownik będzie trzecim argumentem do funkcji url())
# słownik będzie zawsze przekazany do widoku, bez względu na to,
# czy ten widok akceptuje taki argument, więc trzeba uważać

# URL reversing
# nie kodujemy urli na twardo ani nie robimy równoległych mechanizmów ad-hoc
# do uzyskiwania urli, design urli ma być w urlconf - tam wszystkie zmiany urli
# ważna jest nazwa widoku, typy argumentów i ich wartości
# templates: tag url
# kod python: funkcja django.core.urlresolvers.reverse()
# kod (hi-level) obsługi urli dla instancji modeli: metoda get_absolute_url()

# reverse_lazy() pozwala na uzyskanie urla przed załadowaniem urlconf
# wykorzystanie: pozyskiwanie atrybutu url dla generycznego widoku opartego
# na klasie; argument dla dekoratora; domyślna wartość dla signature funkcji

# jeden widok może być wykorzystywany przez kilka urli,
# dlatego trzeba nazywać urle

# dodatkowo używamy namespaces (również dla wielu instancji jednej aplikacji)
# np. klasa AdminSite pozwala na deploy kilku instancji aplikacji admin
# mamy namespace aplikacji - taki sam dla każdej instancji
# mamy namespace instancji - unikalny w projekcie, domyślna wersja instancji
# może mieć taką samą namespace jak aplikacja, np. admin ma admin i admin
# główna strona admina to admin:index
# namespaces można zagnieżdżać, np. members:reviews:index,
# gdzie namespace reviews jest zdefiniowana w obrębie namespace members

# przeszukiwanie namespacowanego urla
# - namespace aplikacji - z tego django dostanie listę instancji
# - jeśli jest zdefiniowana current, django zwraca resolver dla tej instancji
# aplikacja, które ma mieć wiele instacji powinna mieć atrybut
# current_app na przetwarzanym requeście (admin ma request.current_app)
# - może być to również argument dla funkcji reverse()
# - jeśli nie ma current, to django szuka domyślnej (nsp app = nsp inst)
# (w przykładzie reviews jest nsp aplikacji i instancji)
# - jeśli nie ma default, django bierze nazwę ostatnio zdeployowanej instancji
# - jeśli taka nsp nie zgadza się z nsp aplikacji z pierwszego kroku,
# django będzie wyszukiwać bezpośrednio tę nsp jako nsp instancji
# -> dla zagnieżdżonych nsp kroki są przetwarzane dla każdej nsp

# namespaces i inkludowane urlconfigi
# jako argument do inlude: namespace i app_name
# ~ można inkludować obiekt z zagnieżdżonymi danymi namespace
# (app_name może być zmienną w inkludowanym pliku urls)
# inkludowana lista będzie włączona do globalnej namespace, chyba, że
# do include przekażemy krotkę (lista, app_nsp, inst_nsp)
# (musi to być krotka, bo inaczej będą to nienazwane argumenty
# namespace i app_name - jak powyżej; nie będzie wyrzucony wyjątek)
# - admin jest instancją AdminSite, w include podajemy admin.site.urls
# jest to właśnie 3-krotka, zawarta w klasie AdminSite

# advanced templates
# - template - dokument lub zamarkowany string
# - template tag - produkuje zawartość, służy jako instrukcja sterująca,
# pobiera zawartość z bazy danych, umożliwia dostęp do innych tagów
# - template variable - outputuje wartość
# - context - mapowanie name->value przekazane do szablonu, podobne do słownika
# - szablon renderuje kontekst zamieniając zmienne na wartości z kontekstu
# oraz wykonując tagi
# django potrzebuje kontekstu - django.template.Context,

# jest też podklasa django.template.RequestContext
# zawiera ona dodatkowe zmienne, np. obiekt HttpRequest
# lub informacje o zalogowanym użytkowniku (opcja context_processors)

# !!! skrót render() zwraca HttpResponse (nie RequestContext)
# funkcji render() z Template możemy przekazać obiekt RequestContext

# context processors - umożliwiają podanie zmiennych, które będą automatycznie
# ustawiane w każdym kontekście
# żeby skorzystać z custom CP musimy używać RequestContext
# przykład: widoki cp i cpshort

# RequestContext ładuje automatycznie do kontekstu pewne zmienne
# w settings, w TEMPLATES, jest opcja context_processors,
# są to callable, które pobierają request i zwracają słowniki
# ze zmiennymi, które będą częścią kontekstu
# domyślnie jest też uwzględniony cp django.template.context_processors.csrf
# jest on hardcoded i nie może być wyłączony
# procesory są aplikowane w porządku, kolejne zmienne o tej samej nazwie
# zastępują wcześniejsze
# zmienne zaaplikowane przez cp mogą zastąpić zmienne przekazane przez nas
# do RequestContext
# można to obejść
# request_context = RequestContext(request)
# request_context.push({"my_name": "john"})
# custom templates muszą być wymienione w opcji context_processors
# wtedy stają się one globalne
# również w TEMPLATES można określić loadery (loaders)
# w opcji loaders można każdemu loaderowi przypisać folder z szablonami (1.11)
# włączone są loadery z DIRS (django.template.loaders.filesystem.Loader)
# i APP_DIRS (django.template.loaders.app_directories.Loader)
# w produkcji jest włączony cache loader (django.template.loaders.cached.Loader)
# Template możemy używać jeśli deklarujemy korzystanie z jednego
# silnika szablonów, w przeciwnym wypadku używamy get_template()

# render()
# django.template.Template - przyjmuje kontekst: słownik|Context|RequestContext
# django.template.backends.django.Template - przyjmuje: request, context (dict!)
# render() z django.shortcuts - opakowuje powyższy, dodatkowo przyjmuje template
# render_to_response() - content responsa nie zawiera danych requesta
