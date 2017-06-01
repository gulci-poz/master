from django.conf.urls import url
from django.contrib import admin

from .views import current_datetime, hello, hours_ahead, order_notice

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', hello),
    url(r'^hello/$', hello),
    url(r'^time/$', current_datetime),
    url(r'^time/plus/(\d{1,2})/$', hours_ahead),
    url(r'^order_notice/$', order_notice),
]
