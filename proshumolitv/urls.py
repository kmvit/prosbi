from django.conf.urls import patterns, include, url

from django.contrib import admin
from pages.views import PageView
from proshumolitv import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url('^markdown/', include('django_markdown.urls')),

    url(r'', include('requests.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^reminder/', include('reminders.urls')),
    url(r'^prays/', include('prays.urls')),
    url(r'^names/', include('names.urls')),
)

urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))

urlpatterns += patterns('',
    url(r'^(?P<slug>.*)/$', PageView.as_view())
)