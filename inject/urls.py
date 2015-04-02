from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('inject.views',
    url(r'inject_data/$', 'inject_data', name='inject_data'),
)
