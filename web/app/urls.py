from django.conf.urls.defaults import *
from app.views import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #important general shit
    #(r'^admin/', include(admin.site.urls)),
    (r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    #standard pages    
    (r'^$', index),
    (r'^make/$', make),
    (r'^dashboard/$', dashboard),
    (r'^take/(?P<exam_name>.+)/(?P<student_name>.+)/(?P<student_email>.+)/$', take),
    (r'^about/$', about),
    (r'^(?P<exam_name>\w+)/submit_exam/$', submit_exam),
    (r'^(?P<essay_id>\w+)/submit_file/$', submit_file),
    (r'^distribute/(\w+)/$', distribute),
    (r'info_submit/$', info_submit),
    (r'login/$', login),
    (r'logout/$', logout),
    (r'signup/$', signup),
	(r'getfiles/$', getfiles),
 )
