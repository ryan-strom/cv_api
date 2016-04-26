from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    url(r'^flower_detection/detect/$', 'flower_detection.views.detect'),

    url(r'^flower_detection/harris/$', 'flower_detection.views.harrisFeatures'),

    url(r'^flower_detection/shapes/$', 'flower_detection.views.shapes'),

    url(r'^flower_detection/shapes2/$', 'flower_detection.views.shapes2'),

    url(r'^flower_detection/shapes3', 'flower_detection.views.shapes3'),

    url(r'^flower_detection/detect/contours/$', 'flower_detection.views.findContours'),

    url(r'^flower_detection/detect/features/$', 'flower_detection.views.featureDetection'),

    # url(r'^$', 'cv_api.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^species/$', 'flowers.views.getSpecies'),

    url(r'^species/(?P<id>[0-9]+)', 'flowers.views.getSpecies'),

    url(r'^species/create', 'flowers.views.postSpecies'),

    url(r'^species/find', 'flowers.views.findSpecies'),

    url(r'^species/csv', 'flowers.views.csvToDB'),



    url(r'^admin/', include(admin.site.urls)),
)
