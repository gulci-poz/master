from django.conf import settings
from django.conf.urls import include, url, handler404
from django.contrib import admin

from . import views as master_views

# from .views import (hello, current_datetime, hours_ahead, order_notice,
#                     current_datetime_get_template,
#                     current_datetime_render_shortcut,
#                     greeting, utilities_time,
#                     utilities_time_ahead, utilities_request,
#                     utilities_display_meta)

handler404 = 'master.views.handler404'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', master_views.hello),
    url(r'^hello/$', master_views.hello),
    url(r'^time/$', master_views.current_datetime),
    url(r'^time/plus/(?P<offset>\d{1,2})/$', master_views.hours_ahead),
    url(r'^order_notice/$', master_views.order_notice),
    url(r'^time/get-template/$', master_views.current_datetime_get_template),
    url(r'^time/render-shortcut/$',
        master_views.current_datetime_render_shortcut),
    url(r'^greeting/$', master_views.greeting),
    url(r'^utilities/time/$', master_views.utilities_time),
    url(r'^utilities/time/plus/(?P<offset>\d{1,2})/$',
        master_views.utilities_time_ahead),
    # /utilities/request/?bla=bla&name=user
    url(r'^utilities/request/$', master_views.utilities_request),
    url(r'^utilities/request/meta/$', master_views.utilities_display_meta),
    # apps urls root
    url(r'^books/', include('books.urls', namespace='books')),
    url(r'^contact/', include('contact.urls', namespace='contact')),
    # testing
    url(r'^testing/(?P<num>\d?)$', master_views.testing,
        {'meta': 'testing'}, name='testing'),
    url(r'^cp/$', master_views.cp, name='cp'),
    url(r'^cpshort/$', master_views.cpshort, name='cpshort'),
    url(r'^cpglobal/$', master_views.cpglobal, name='cpglobal'),
]

if settings.DEBUG:
    urlpatterns += [url(r'^debuginfo/$', master_views.debug), ]
