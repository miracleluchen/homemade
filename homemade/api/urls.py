from django.conf.urls import patterns, include, url
from django.contrib import admin
from homemade.decorators import logger_for_view
from django.conf import settings
from django.contrib.auth.decorators import login_required
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hris.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Angular
    # (r'^hris_web/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.BASE_DIR + '/hris_web/'}),

    url(r'^cooker/$', logger_for_view(views.GetUserListView.as_view(), "GetCookerListView"), name="getCookerList"),
    url(r'^tag/$', logger_for_view(views.GetTagListView.as_view(), "GetTagListView"), name="getTagList"),
    url(r'^tag/(?P<pk>\d+)/food/$', logger_for_view(views.GetFoodListByTagView.as_view(), "GetFoodListByTagView"), name="getFoodListByTag"),
)