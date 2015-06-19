from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns(
	'',
    url(r'^admin/', include(admin.site.urls)),
)

if 'api' in settings.INSTALLED_APPS:
    urlpatterns += (url(r'^api/', include(
            'api.urls', namespace='api')),)