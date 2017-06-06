from django.conf.urls import url

from . import views as contact_views

urlpatterns = [
    url(r'^$', contact_views.contact, name='contact-form'),
    url(r'^thanks/$', contact_views.contact_thanks, name='contact-thanks'),
]
