# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls.defaults import *

from views import home, thanks, beta, invite, buckettalk, template, featured, test2, start, token, register, login, logout, profile, profileajax, sendmail, whitlist, newitem, saveitem, terms, addfriends, rushmore, bike, whits, google, sitemapxml,rpx, view404, view500
#import django_rpx.views

handler404 = 'views.view404'
handler500 = 'views.view500'

urlpatterns = patterns('',
#    (r'^$', my_homepage_view),
    (r'^$', home),
    (r'^thanks/$', thanks),
    (r'^beta/$', beta),
    (r'^invite/$', invite),
    (r'^buckettalk/$', buckettalk),
    (r'^template/$', template),
    (r'^featured/$', featured),
    (r'^test2/$', test2),
    (r'^start/$', start),
    (r'^token/$', token),
    (r'^register/$', register),
    (r'^login/$', login),
    (r'^logout/$', logout),
    (r'^profile/$', profile),
    (r'^profileajax/$', profileajax),
    (r'^sendmail/$', sendmail),
    (r'^whitlist/$', whitlist),
    (r'^newitem/$', newitem),
    (r'^saveitem/$', saveitem),
    (r'^terms/$', terms),
    (r'^addfriends/$', addfriends),
    (r'^whits/(?P<page>.+)/$', whits),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/favicon.ico'}),
    (r'^apple-touch-icon\.png$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/apple-touch-icon.png'}),
    (r'^apple-touch-icon-precomposed\.png$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/apple-touch-icon-precomposed.png'}),
    (r'^google6f66e7791a1c9df8.html', google),
    (r'^sitemap.xml', sitemapxml),
    (r'^rpx_xdcomm.html', rpx),
    
#    ('/rest/.*', rest.Dispatcher),
#    (r'^accounts/', include('django_rpx_plus.urls')),
#    (r'', include('openidgae.urls')),
    # Example:
    # (r'^foo/', include('foo.urls')),

    # Uncomment this for admin:
#    (r'^admin/', include('django.contrib.admin.urls')),
#    url(r'^rpx_response/$', 'rpx_response', name='rpx_response'),
#    url(r'^login/$', 'login', name='auth_login'),
#    url(r'^register/$', 'register', name='auth_register'),
#    url(r'^associate/$', 'associate', name='auth_associate'),
#    url(r'^associate/delete/(\d+)/$', 'delete_associated_login', name='auth_delete_associated'),
#    url(r'^associate/rpx_response/$', 'associate_rpx_response', name='associate_rpx_response'),
)
