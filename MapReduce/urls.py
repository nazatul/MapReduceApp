from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MapReduce.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$','MapReduceApp.views.home'),
)
