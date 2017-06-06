from django.shortcuts import render

from .models import Book


def books_search(request):
    error = False

    if 'q' in request.GET:
        q = request.GET['q']

        if not q:
            error = True
        else:
            result = Book.objects.filter(title__icontains=q)
            return render(request, 'books/search_result.html',
                          {'current_section': 'books-search-result',
                           'query': q,
                           'result': result,
                           })

    return render(request, 'books/search_form.html',
                  {'current_section': 'books-search-form',
                   'error': error
                   })
