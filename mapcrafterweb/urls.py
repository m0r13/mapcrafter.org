from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mapcrafterweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r"^(|index\.html)$", views.index, name="index"),
    url(r"^downloads\.html$", views.downloads, name="downloads"),
)
