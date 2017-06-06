from django.shortcuts import render

from .models import Book


def books_search(request):
    errors = []

    if 'q' in request.GET:
        q = request.GET['q']

        if not q:
            errors.append('Enter a search term.')
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            result = Book.objects.filter(title__icontains=q)
            return render(request, 'books/search_result.html',
                          {'current_section': 'books-search-result',
                           'query': q,
                           'result': result,
                           })

    return render(request, 'books/search_form.html',
                  {'current_section': 'books-search-form',
                   'errors': errors
                   })
