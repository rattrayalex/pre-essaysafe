from django.conf.urls.defaults import *
from django.contrib import admin

import app

admin.autodiscover()

urlpatterns = patterns('',
    (r'^google/oauth/', include('google_oauth.urls', namespace='google_oauth', app_name='google_oauth'))
    (r'^app/', include(app.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    )
