from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('inject.views',
    url('^/', 'inject_data', name='inject_data'),
)
