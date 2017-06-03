from django.conf.urls import url
from django.contrib import admin

from .views import (hello, current_datetime, hours_ahead, order_notice,
                    current_datetime_get_template,
                    current_datetime_render_shortcut, greeting)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', hello),
    url(r'^hello/$', hello),
    url(r'^time/$', current_datetime),
    url(r'^time/plus/(\d{1,2})/$', hours_ahead),
    url(r'^order_notice/$', order_notice),
    url(r'^time/get-template/$', current_datetime_get_template),
    url(r'^time/render-shortcut/$', current_datetime_render_shortcut),
    url(r'^greeting/$', greeting),
]
