from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mapcrafterweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r"^admin/", include(admin.site.urls)),
    url(r"^blog/", include("zinnia.urls", namespace="zinnia")),
    url(r"^comments/", include("django_comments.urls")),
    url(r"^", include("mapcrafterweb.urls", namespace="mapcrafterweb")),
)
