from django.conf.urls import patterns, include, url
from names.views import LiveSearchNames, UpdateName

urlpatterns = patterns('',
    url(r'^live_search/$', LiveSearchNames.as_view(), name='live_search_names'),
    url(r'^add/(\d+)/$', 'names.views.add_names', name='add_names'),
    url(r'^name_register/(?P<pk>\d+)/$', UpdateName.as_view(), name='name_register'),
)
