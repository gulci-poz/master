from django.conf.urls import url
from django.contrib import admin

from .views import hello

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', hello),
    url(r'^hello/$', hello),
]
