from django.conf.urls import patterns, include, url
from django.conf import settings

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

if settings.DEBUG:
    urlpatterns += patterns('',
                           (r'^library/(?P<path>.*)$', 'django.views.static.serve', {
                            'document_root': settings.MEDIA_ROOT}),
                            )

urlpatterns += patterns('',
                        url(r'^$', 'pyWriter.lib.apps.story.views.index'),
                        )

urlpatterns += patterns('',
                        url(r'^tinymce/', include('tinymce.urls')),
                        )

urlpatterns += patterns('',
                        url(
                        r'^login/$', 'pyWriter.lib.apps.login.views.login_view',
                        name="login_view"),
                        url(r'^logout/$',
                            'pyWriter.lib.apps.login.views.logout_view'),
                        url(
                        r'^signup/$', 'pyWriter.lib.apps.login.views.create_user_view',
                        name="signup"),
                        )

urlpatterns += patterns('',
                        url(
                        r'^scene/add/$', 'pyWriter.lib.apps.story.views.scene',
                        name="add_scene"),
                        url(r'^scene/(?P<scene>\d+)/$',
                            'pyWriter.lib.apps.story.views.scene', name="edit_scene"),
                        )
urlpatterns += patterns('',
                        url(
                        r'^story/add/$', 'pyWriter.lib.apps.story.views.story',
                        name="add_story"),
                        url(r'^story/(?P<story>\d+)/$',
                            'pyWriter.lib.apps.story.views.story', name="edit_story"),
                        )
urlpatterns += patterns('',
                        url(
                        r'^chapter/add/$', 'pyWriter.lib.apps.story.views.chapter',
                        name="add_chapter"),
                        url(r'^chapter/(?P<chapter>\d+)/$',
                            'pyWriter.lib.apps.story.views.chapter', name="edit_chapter"),
                        )
urlpatterns += patterns('',
                        url(
                        r'^character/add/$', 'pyWriter.lib.apps.story.views.character',
                        name="add_character"),
                        url(r'^character/(?P<character>\d+)/$',
                            'pyWriter.lib.apps.story.views.character', name="edit_character"),
                        )
urlpatterns += patterns('',
                        url(
                        r'^location/add/$', 'pyWriter.lib.apps.story.views.location',
                        name="add_location"),
                        url(r'^location/(?P<location>\d+)/$',
                            'pyWriter.lib.apps.story.views.location', name="edit_location"),
                        )
urlpatterns += patterns('',
                       url(
                           r'^artifact/add/$', 'pyWriter.lib.apps.story.views.artifact',
        name="add_artifact"),
        url(r'^artifact/(?P<artifact>\d+)/$',
            'pyWriter.lib.apps.story.views.artifact', name="edit_artifact"),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
   )
