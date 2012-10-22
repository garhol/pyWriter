from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',)

urlpatterns += patterns('',
    # Examples:
    # url(r'^$', 'pyWriter.views.home', name='home'),
    # url(r'^pyWriter/', include('pyWriter.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
	url(r'^$', 'pyWriter.lib.apps.story.views.index'),
)

urlpatterns += patterns('',
   url(r'^login/$', 'pyWriter.lib.apps.login.views.login_view', name="login_view"),
   url(r'^logout/$', 'pyWriter.lib.apps.login.views.logout_view'),
)

