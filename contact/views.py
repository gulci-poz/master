from django.core.mail import get_connection, send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import ContactForm


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            con = get_connection(
                'django.core.mail.backends.console.EmailBackend')
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'),
                ['siteowner@example.com'],
                connection=con
            )

            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm(initial={'subject': 'I love your site!'})

    return render(request, 'contact/contact_form.html',
                  {'current_section': 'contact-form', 'form': form})


def contact_thanks(request):
    return render(request, 'contact/contact_thanks.html',
                  {'current_section': 'contact-thanks',
                   'message': 'Thank you for submitting your message.'})
