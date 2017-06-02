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

# zadania szablonów:
# - separacja logiki od designu
# - DRY
# - bezpieczeństwo - zakaz wykonywania kodu
