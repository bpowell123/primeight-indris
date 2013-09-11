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

"""Bootstrap for running a Django app under Google App Engine.

The site-specific code is all in other files: settings.py, urls.py,
models.py, views.py.  And in fact, only 'settings' is referenced here
directly -- everything else is controlled from there.

"""

## Standard Python imports.
#import os
#import sys
#import logging
#
#from appengine_django import InstallAppengineHelperForDjango
#InstallAppengineHelperForDjango()
#
#from appengine_django import have_django_zip
#from appengine_django import django_zip_path
#
## Google App Engine imports.
#from google.appengine.ext.webapp import util
#
## Import the part of Django that we use here.
#import django.core.handlers.wsgi
#
#def main():
#  # Ensure the Django zipfile is in the path if required.
#  if have_django_zip and django_zip_path not in sys.path:
#    sys.path.insert(1, django_zip_path)
#
#  # Create a Django application for WSGI.
#  application = django.core.handlers.wsgi.WSGIHandler()
#
#  # Run the WSGI CGI handler with that application.
#  util.run_wsgi_app(application)
#
#if __name__ == '__main__':
#  main()


from datetime import datetime
import os
import sys
import logging
import urllib
import simplejson
import custom_filters
#import rest
#from google.appengine.dist import use_library
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
#use_library('django', '1.2')

from appengine_django import InstallAppengineHelperForDjango
InstallAppengineHelperForDjango()

# Google App Engine imports.
from google.appengine.ext.webapp import util

from appengine_django import have_django_zip
from appengine_django import django_zip_path

# Import the part of Django that we use here.
import django.core.handlers.wsgi

from google.appengine.api import urlfetch, users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.db import djangoforms

from gaesessions import get_current_session

# configure the RPX iframe to work with the server were on (dev or real)
ON_LOCALHOST = ('Development' == os.environ['SERVER_SOFTWARE'][:11])
if ON_LOCALHOST:
    import logging
    logging.warn( type(os.environ['SERVER_PORT']))
    if os.environ['SERVER_PORT'] == '80':
        BASE_URL = 'localhost'
    else:
        BASE_URL = 'localhost:%s' % os.environ['SERVER_PORT']
else:
    BASE_URL = 'dowhit.com'

def redirect_with_msg(h, msg, dst='/'):
    get_current_session()['msg'] = msg
    h.redirect(dst)

# create our own simple users model to track our user's data
class MyUser(db.Model):
    created         = db.DateTimeProperty(auto_now_add=True)
    email           = db.EmailProperty()
    display_name    = db.StringProperty(required=False)
    past_view_count = db.IntegerProperty(default=0) # just for demo purposes ...
    firstName       = db.StringProperty(required=False)
    lastName        = db.StringProperty(required=False)
    dob             = db.DateProperty(required=False)
    gender          = db.StringProperty(required=False)
    ethnicity       = db.StringProperty(required=False)
    country         = db.StringProperty(required=False)
    state           = db.StringProperty(required=False)
    zip             = db.StringProperty(required=False)
    smoker          = db.BooleanProperty(default=False)
    height          = db.IntegerProperty(required=False)
    weight          = db.IntegerProperty(required=False)
    bmi             = db.FloatProperty(required=False)
    outlook         = db.StringProperty(required=False)
    bp              = db.StringProperty(required=False)
    cholesterol     = db.IntegerProperty(required=False)
    profilePic      = db.LinkProperty(default = "http://" + BASE_URL + "/static/images/dowhitO.png")
    provider        = db.StringProperty(required=False)
    profileURL      = db.LinkProperty(required=False)
    location        = db.StringProperty(required=False)
    whitDays        = db.IntegerProperty(default=28380)
    authorized      = db.BooleanProperty(default=False)
    agree           = db.BooleanProperty(default=False)
    emailAccount    = db.BooleanProperty(default=False)
    emailOffers     = db.BooleanProperty(default=False)
    inviteCode      = db.StringProperty(required=False)

class FutureUser(db.Model):
    created         = db.DateTimeProperty(auto_now_add=True)
    firstName       = db.StringProperty(required=False)
    email           = db.EmailProperty()
    dob             = db.DateTimeProperty()
    gender          = db.StringProperty()

class MyUserFriends(db.Model):
    user            = db.ReferenceProperty(MyUser, collection_name='users')
    friend          = db.ReferenceProperty(MyUser, collection_name='friends')
    status          = db.StringProperty(choices=('pending','approved'))

class UserForm(djangoforms.ModelForm):
    class Meta:
        model = MyUser
#        exclude = ['added_by']

class WhitList(db.Model):
    user            = db.ReferenceProperty(MyUser, collection_name='whitLists')
    name            = db.StringProperty()
    created         = db.DateTimeProperty(auto_now_add=True)
    private         = db.BooleanProperty(default=False)

class WhitListItem(db.Model):
    whitList        = db.ReferenceProperty(WhitList, collection_name='whitListItems')
    name            = db.StringProperty()
    added           = db.DateTimeProperty(auto_now_add=True)
    sortOrder       = db.IntegerProperty()
    desc            = db.TextProperty()
    tag             = db.StringListProperty(default=[])#unicode,default=['Adventure','Career','Community','Culture and Arts','Education','Entertainment','Family','Fitness','Health and Wellness','Hobbies','Home Improvement','Issues and Causes','Literature','Music','Outdoor Recreation','Relationships','Spiritual','Sports','Travel','Wealth and Finance'])
    accomplishBy    = db.DateProperty()
    rank            = db.RatingProperty()
    cost            = db.FloatProperty()
    status          = db.StringProperty(choices=('open', 'completed'))
    accomplishDate  = db.DateProperty()
    private         = db.BooleanProperty(default=False)
    flickrImage     = db.TextProperty(default="")
    location        = db.StringProperty(default="")
    referringItem   = db.StringProperty(default=None)
    addedTotal      = db.IntegerProperty(default=1)
    completedTotal  = db.IntegerProperty(default=0)

class WhitItemLink(db.Model):
    item            = db.ReferenceProperty(WhitListItem, collection_name='links')
    link            = db.LinkProperty()

class WhitItemPic(db.Model):
    item            = db.ReferenceProperty(WhitListItem, collection_name='pics')
    link            = db.LinkProperty()

class WhitItemComment(db.Model):
    item            = db.ReferenceProperty(WhitListItem, collection_name='comments')
    comment         = db.TextProperty()
    timestamp       = db.DateTimeProperty(auto_now_add=True)

def main():
  # Ensure the Django zipfile is in the path if required.
  if have_django_zip and django_zip_path not in sys.path:
    sys.path.insert(1, django_zip_path)

  # Create a Django application for WSGI.
  application = django.core.handlers.wsgi.WSGIHandler()

  # Run the WSGI CGI handler with that application.
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()