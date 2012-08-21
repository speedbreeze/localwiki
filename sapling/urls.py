from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic.simple import redirect_to
from django.contrib.admin.views.decorators import staff_member_required

import pages
import maps
import redirects
import dashboard
from users.admin import SubscribedList

admin.autodiscover()

urlpatterns = patterns('',
    (r'^map/', include(maps.site.urls)),
    (r'^tags$', redirect_to, {'url': '/tags/'}),
    (r'^tags/', include('sapling.tags.urls', 'tags', 'tags')),
    (r'^attributes$', redirect_to, {'url': '/attributes/'}),
    (r'^attributes/', include('sapling.infobox.urls', 'infobox', 'infobox')),
    (r'^_redirect/', include(redirects.site.urls)),
    (r'^(?i)Users/', include('sapling.users.urls')),
    (r'^search/', include('sapling.search.urls')),
    (r'^', include('sapling.recentchanges.urls')),
    (r'^tools/', include(dashboard.site.urls)),

    # JS i18n support.
    (r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),

    (r'^admin$', redirect_to, {'url': '/admin/'}),
    (r'^admin/subscribers/$', staff_member_required(SubscribedList.as_view())),
    (r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# This should only happen if you're using the local dev server with
# DEBUG=False.
if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    )

# Fall back to pages.
urlpatterns += patterns('',
    (r'^', include(pages.site.urls)),
)
