from django.conf.urls import patterns, include, url
from prays.views import PrayView, PrayListView, PrayerBookView, DeletePrayerBookItem, SelfPrayerBookView, PrayCategoryListView

from requests.views import RequestListView, AddRequest, AddPrayEvent, RequestPrayersList, RequestView, AddComment


urlpatterns = patterns('',
    url(r'^$', PrayListView.as_view(), name='prays'),
    url(r'^categories/$', PrayCategoryListView.as_view(), name='pray_categories'),
    url(r'^book/(?P<pk>\d+)/$', PrayerBookView.as_view(), name='prayer_book'),
    url(r'^book/my/$', SelfPrayerBookView.as_view(), name='prayer_book_my'),
    url(r'^delete/(?P<pk>\d+)/$', DeletePrayerBookItem.as_view(), name='delete_prayer_book_item'),
    url(r'^move/(\d+)/$', 'prays.views.move_prayerbook_item', name='move_prayerbook_item'),
    url(r'^add_pray/(\d+)/$', 'prays.views.add_pray_to_prayerbook', name='add_pray_to_prayerbook'),
    url(r'^export/pray/pdf/(\d+)/$', 'prays.views.export_pray_PDF', name='export_pray_pdf'),
    url(r'^export/prayerbook/pdf/(\d+)/$', 'prays.views.export_prayerbook_PDF', name='export_prayerbook_pdf'),
    url(r'^(?P<slug>[\w\d]+)/$', PrayView.as_view(), name='pray'),

)