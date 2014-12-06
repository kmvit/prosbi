from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('account.views',
    url(r'^signup/', 'sign_up', name='signup'),
    url(r'^register/(\w+)/', 'register', name='register'),
    url(r'^login/', 'login', name='login'),
    url(r'^logout/', 'logout', name='logout'),

)
