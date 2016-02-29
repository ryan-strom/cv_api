from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:

    url(r'^flower_detection/detect/$', 'flower_detection.views.detect'),

    url(r'^flower_detection/detect/contours/$', 'flower_detection.views.findContours'),

    # url(r'^$', 'cv_api.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
