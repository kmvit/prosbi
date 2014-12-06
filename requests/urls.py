from django.conf.urls import patterns, include, url

from requests.views import RequestListView, AddRequest, AddPrayEvent, RequestPrayersList, RequestView, AddComment


urlpatterns = patterns('',
    url(r'^$', RequestListView.as_view(), name='requests'),
    url(r'^page/(?P<page>\d+)/$', RequestListView.as_view(), name='requests'),
    url(r'^(?P<pk>\d+)/$', RequestView.as_view(), name='request'),

    url(r'^add/$', AddRequest.as_view(), name='add_request'),
    url(r'^add_pray_event/$', AddPrayEvent.as_view(), name='add_pray_event'),
    url(r'^get_request_prayer_list/(?P<pk>\d+)/$', RequestPrayersList.as_view(), name='get_request_prayer_list'),

    url(r'^add_comment/$', AddComment.as_view(), name='add_comment'),
)