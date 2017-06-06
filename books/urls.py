from django.conf.urls import url

from . import views as books_views

urlpatterns = [
    url(r'^search/$', books_views.books_search,
        name='books-search'),
]
