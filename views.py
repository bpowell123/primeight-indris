from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse
import django.http as http
import datetime
import os
import time
import cgi
import urllib, hashlib
import urllib2, base64
import urlparse
import re
try:
    import json
except ImportError:
    import simplejson as json
import simplejson as json
import main
import datecalc
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.db import djangoforms
from main import MyUser, FutureUser, MyUserFriends, UserForm, WhitList, WhitListItem, WhitItemLink, WhitItemPic, WhitItemComment
from gaesessions import get_current_session
from django.contrib.humanize.templatetags.humanize import intcomma

from django.conf import settings
import django.contrib.auth as auth
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from urlparse import urlparse

#The reason why we use django's urlencode instead of urllib's urlencode is that
#django's version can operate on unicode strings.
from django.utils.http import urlencode

#countdown_date = "2010-9-21 20:30:00 GMT-04:00"

# configure the RPX iframe to work with the server were on (dev or real)
ON_LOCALHOST = ('Development' == os.environ['SERVER_SOFTWARE'][:11])
#if ON_LOCALHOST:
#    import logging
#    logging.warn( type(os.environ['SERVER_PORT']))
#    if os.environ['SERVER_PORT'] == '80':
#        BASE_URL = '127.0.0.1'
#    else:
#        BASE_URL = "127.0.0.1:" + os.environ['SERVER_PORT']
#else:
BASE_URL = os.environ['HTTP_HOST']#'www.dowhit.com'

def glvars(x,y):
    x.update(y)
    return x

def getSessionUser(request):
    session = get_current_session()
    adjDays = 0
    if session.has_key('me'):
        currentUser = MyUser()
        currentUser = session['me']
        
        if currentUser.display_name is not None:
            greeting = ("<img class=\"thumb\" src=\"%s\"/>&nbsp;&nbsp;&nbsp;%s " % 
                        (currentUser.profilePic, currentUser.display_name))
            profileLink = ("<a href=\"/profile/\">%s</a>" %
                           (greeting))
            logLink = "<a href=\"/logout/\">SIGN OUT</a>"
        else:
            greeting = ""
            profileLink = ""
            re = os.environ.get('PATH_INFO')
#            logLink = greeting + "<a class=\"rpxnow\" onclick=\"return false;\" href=\"https://dowhit.rpxnow.com/openid/v2/signin?token_url=http%3A%2F%2F" + BASE_URL + "%2Ftoken%2F&amp;redirect=" + re + "\"> Sign In</a>"
#            logLink = greeting + "<a class=\"poplight\" rel=\"popup_login\" onclick=\"return false;\" href=\"#?w=330\"> Sign In</a>"
            logLink = greeting + "<a class=\"janrainEngage\" href=\"#\"> SIGN IN</a>"
       
        current_date = time.strftime("%B %d, %Y",time.localtime())
        if currentUser.dob is not None:
            now = datetime.date.today()
            adjDays = datecalc.getAdjDays(currentUser)
            #adjDays = ((0.00004681401833 * (AGE**3)) - (0.003268056416 * (AGE**2)) - (0.8978485239 * AGE) + 77.76649053) * 365.4
            curD = now + datetime.timedelta(days=adjDays)
            y = curD.strftime("%Y")
            m = int(curD.strftime("%m"))
            m = str(m)
            d = curD.strftime("%d")
            h = "0"
            mn = "0"
            s = "0"
            countdown_date = curD.strftime("%Y-%m-%d %H:%M:%S GMT-05:00")
            adjDays = adjDays - 1
        else:
            y = "2011"
            m = "11"
            d = "17"
            h = "11"
            mn = "11"
            s = "11"
            countdown_date = "2011-1-1 00:00:00 GMT-05:00"

    else:
        greeting = ""
        profileLink = ""
        currentUser = ""
        re = os.environ.get('PATH_INFO')
#        logLink = greeting + "<a class=\"poplight\" rel=\"popup_login\" onclick=\"return false;\" href=\"#?w=330\"> Sign In</a>"
#        logLink = greeting + "<a class=\"rpxnow\" onclick=\"return false;\" href=\"https://dowhit.rpxnow.com/openid/v2/signin?token_url=http%3A%2F%2F" + BASE_URL + "%2Ftoken%2F\"> Sign In</a>"
        logLink = greeting + "<a class=\"janrainEngage\" href=\"#\"> SIGN IN</a>"

        y = "2011"
        m = "11"
        d = "17"
        h = "11"
        mn = "11"
        s = "11"
        current_date = time.strftime("%B %d, %Y",time.localtime())
        countdown_date = "2011-1-1 00:00:00 GMT-05:00"

    return profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays

def home(request):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)
     
    if currentUser and currentUser.authorized:
        return redirect('/featured/', glvars(locals(), globals()))
    else:

        if request.method == 'POST': # If the form has been submitted...
    
            FUser = FutureUser()
            form = cgi.FieldStorage()
            FUser.email = form.getvalue("email")
            FUser.firstName = form.getvalue("first-name")
            FUser.dob =  datetime.datetime.strptime(form.getvalue("dob"),"%m/%d/%Y")
            FUser.gender = form.getvalue("gender")
    
    #        FUser.put()
            
            u = MyUser()
            u.dob = FUser.dob.date()
            u.gender = FUser.gender
    #        u.email = FUser.email               
            
            if session.has_key('me'):
                session['me'] = u
                return redirect('/profile/', glvars(locals(),globals()))
            else:
                session['me'] = u
                return redirect('/#login', glvars(locals(),globals())) # Redirect after POST

    body_content = "Home"
    return render_to_response('layouts/home.html', glvars(locals(),globals()))

def thanks(request):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)


    body_content = "Thanks"
    return render_to_response('layouts/thanks.html', glvars(locals(),globals()))

def beta(request):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)


    body_content = "Beta"
    return render_to_response('layouts/beta.html', glvars(locals(),globals()))

def invite(request):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)
    
    if not currentUser:
        return redirect('/', glvars(locals(), globals()))

    if request.method == 'POST': # If the form has been submitted...

        form = cgi.FieldStorage()
        if str(form.getvalue("invite")).upper() in ["ZG93AGL0", "PITT262"]:
            currentUser.authorized = True
            currentUser.inviteCode = form.getvalue("invite")

            currentUser.put()
    
            session['me'] = currentUser
            
            return redirect('/whitlist/', glvars(locals(), globals()))
        else:
            return redirect('/profile/#complete?error=invalid', glvars(locals(), globals()))

def buckettalk(request):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)


    body_content = "Bucket Talk"
    return render_to_response('layouts/buckettalk.html', glvars(locals(),globals()))

def view404(request):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)

    body_content = "Page Not Found"
    return render_to_response('layouts/404.html', glvars(locals(),globals()))

def view500(request):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)

    body_content = "Error"
    return render_to_response('layouts/500.html', glvars(locals(),globals()))

def google(request):
    return render_to_response('layouts/google6f66e7791a1c9df8.html', glvars(locals(),globals()))

def sitemapxml(request):
    return render_to_response('layouts/sitemap.xml', glvars(locals(),globals()))

def rpx(request):
    return render_to_response('layouts/rpx_xdcomm.html', glvars(locals(),globals()))

def addfriends(request):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)


    ulist = dict();
    q = MyUser.all();
    for u in q:
        ulist[u.key()] = u.display_name;
#            ulist.append(u.display_name:)

    if request.method == 'POST': # If the form has been submitted...

        muf = MyUserFriends();

        form = cgi.FieldStorage()
        muf.user = db.Key(form.getvalue("User"))
        muf.friend = db.Key(form.getvalue("Friend"))
        muf.status = form.getvalue("Status")

        muf.put()

    body_content = "addfriends"
    return render_to_response('layouts/addfriends.html', glvars(locals(),globals()))

def template(request):
    body_content = "Template"
    return render_to_response('layouts/template.html', glvars(locals(),globals()))

def rushmore(request):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)
    body_content = "Rushmore"
    return render_to_response('shared/rushmore.html', glvars(locals(),globals()))

def bike(request):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)
    body_content = "Bike"

    #This file was modified on 1/19/2011
    return render_to_response('shared/cross_country_bike.html', glvars(locals(),globals()))

def whits(request, page):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)
    body_content = "whits"

    #This file was modified on 1/19/2011
    return render_to_response('shared/' + page + '.html', glvars(locals(),globals()))

def terms(request):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)
    body_content = "Terms of Use"
    return render_to_response('layouts/terms.html', glvars(locals(),globals()))

def register(request):
    body_content = "Register"
    return render_to_response('layouts/register.html', glvars(locals(),globals()))

def login(request):
    body_content = "Login"
    return render_to_response('layouts/login.html', glvars(locals(),globals()))

def prefetch_refprops(entities, *props):
    fields = [(entity, prop) for entity in entities for prop in props]
    ref_keys = [prop.get_value_for_datastore(x) for x, prop in fields]
    ref_entities = dict((x.key(), x) for x in db.get(set(ref_keys)))
    for (entity, prop), ref_key in zip(fields, ref_keys):
        prop.__set__(entity, ref_entities[ref_key])
    return entities

def featured(request):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)
    
    if not currentUser:
        return redirect('/', glvars(locals(), globals()))

    if not currentUser.authorized:
        return redirect('/profile/', glvars(locals(), globals()))
    else:
        if session.has_key('wl'):
            wList = WhitList()
            wList = session['wl']
    
        form = cgi.FieldStorage()
        if form.getvalue("category") is not None:
            category = form.getvalue("category")
            q = db.GqlQuery("SELECT * FROM WhitListItem where referringItem =:1 AND tag=:2 ORDER BY addedTotal DESC", None, category)
            cacheKey = category + "Items"
        else :
            q = db.GqlQuery("SELECT * FROM WhitListItem where referringItem =:1 ORDER BY addedTotal DESC", None)
            cacheKey = "Items"
            
        results = memcache.get(cacheKey)
        if results is None:
            results = q.fetch(100)
            prefetch_refprops(results, WhitListItem.whitList)
            memcache.add(cacheKey, results, 3600)
                 
        ilist = []
        slist = []
        scriptHtml = ""
        
        wl = WhitList()
        u = MyUser()
        count = 0
        
#        wlItems = memcache.get()
#        if wlItems is None:
#            wlItems = wList.whitListItems
#            memcache.add(wList.)        
#        wList.whitListItems
        
        for index in range(len(results)):
            wl = results[index].whitList
            u = wl.user
            item = WhitListItem()
            for myItem in wList.whitListItems:
                count = count + 1
                if myItem.name.upper() == results[index].name.upper():
                    if myItem.status == 'completed':
                        buttonHtml = "<div class=\"green_font float_right\">You DIDit!</div>"
                        break                                                        
                    else:
                        buttonHtml = "<div class=\"green_font float_right\"><form name=\"newitem%s\" action=\"/newitem/\" method=\"post\"><p><input name=\"newName\" type=\"hidden\" value=\"%s\"><input name=\"newItem\" type=\"hidden\" value=\"%s\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type=\"image\" id=\"done\" name=\"done\" alt=\"I DIDit\" title=\"I DIDit\" onclick=\"return(shareList)\" src=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAK8AAACvABQqw0mAAAABh0RVh0U29mdHdhcmUAQWRvYmUgRmlyZXdvcmtzT7MfTgAABDBJREFUWIXdl2toHFUUx//n3tnd7MZuQmiCTSJqrLWuqKGQWiW2USGFFBKtMVW/+IAWjE2p1SqoqOAX/VCrTalEbX1B2igRWgW/iC2ipM07FmJtjU2QQpI1SbPZ18zchx+ySfeZhyQWO3CY3Z175ve795zZy5DWGlfzYFeVfs0LHGyj3KZ2Y/1cY2i5euBI963lDl7SwshRqLT5S8Tq3b2jzN/5nwh81rPBxymvLSqHvEKNwcmL4eSrtFSX3x0J/PzWK5u0uWwCn3T5rnfwmzrD9vkiIcfByAmlTXC2Am7HbZA68HXHX+11TTXT3CXtgddOEnFe0hqyhopMMQkNN6Rm0PDAVhYC0V8RsYerbi9YyWdyjKUUuCVny/tRe+S+qO0HsSxIpQHQFRQRSFPD7nv9cskFDndXP2bL4K6gdQmELEAhDg4QCIwcDbs2/PFpfN6S9MDHXVWFUqvfAtHfvRoKlKayBPbG3vKBt5N/z7gC77WVVWc7VtXbKnx25/of9s4lILXxxZR50SuUAlHqLRmxL18uv5ACBzI04YEzlY+7HcXHoyK0GXC9dKijuiUTvKnz0Z1he/yhiJiCghNSs4RQmneHdc4zmfJTStDYXvUEI2fzePg8bBUCgZDrXg0X935VX/bNtvixH3bV3miJYP9EZMDDKN1cKGiQ685XN/YNZhJIyDpw5pGNgKvZH7wASwoAHmi4MRYaRMSeqmts35qwEkKKI5PREY9UBKFYSmjt2D4XPEVgMjJ6/0hgAFFbQEoDQhCEIEjlxOjUIMJWsO6D01uPTcvWbp+KTjwYMkMJY2dzBD/6ZsXZY3PBgaQSvPj9mhKCcZpA+ekGS21jZfbNyHbl9UXtwFp/8E9X2o4nGmXkXvPO5o7JRQkAwAvf3eXTWp0CkFZCaYm87CKEzAlYMpL2kePMqN23pbd1PnhaAQBoOH63T2l1EkBBSgIAqQWIOBgIydlE7NuDNX3VC4EDGR7Dxpq+fimNB4Qgv5CE+LAlQSkHpGSwk64JyUJQWc8tFA7M80/4bEupT6nM5Ug+OOPPH97Wc2jJBADgyc9LfWqOnpi9Eaj96NN99ywGDixgO25+qrffsliFacJvmoBlpYZpQQvbsWOxcGARm9HDH61ba1viJxDyMbPLxlI5Y/tP1Pfu+TcCaTcjgwgxxExAaH2ucn/pJqXVKTAUQE1fIdAlaTtfJyKDX9GKn9XMdy3STJa01jCInAC8ADwAnAAcMTkGgMfOJIGJGyoK1hVX5O9jWbwYQltjPYE951qHfuRATjwsFgqAjJ0FABuABSAMICC0tuIFcgFkA3DF4EYcnM+shgRCnhVZ3sLKgjuCF8PDw91/D3HguhgkfvY6Di5jAgKACSAE4PKswDzLn1AKApgApNbaJiLGp4XjocmfEyK5DMv2XrDQ49p+NftfCPwDIKskFDb/Fv8AAAAASUVORK5CYII=\" class=\"addButton\"></p></form></div>" % (index, results[index].name, results[index].key())
                        break
                else :
                    buttonHtml = "<div class=\"green_font float_right\"><form name=\"newitem%s\" action=\"/newitem/\" method=\"post\"><p><input name=\"newName\" type=\"hidden\" value=\"%s\"><input name=\"newItem\" type=\"hidden\" value=\"%s\"><input type=\"image\" id=\"add\" name=\"add\" alt=\"I want to DOwhit\" title=\"I want to DOwhit\" onclick=\"return(shareList)\" src=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAK8AAACvABQqw0mAAAABh0RVh0U29mdHdhcmUAQWRvYmUgRmlyZXdvcmtzT7MfTgAAAzBJREFUWIXFl8+LHEUUxz+vu2d2dnF2/XUKuJCLqxFMiEJQQTAHRSQ3j3rw4p485CAYb6KoeDAHb6L/gYI3TxEF8eYvEEXFqMlBPGTN7M/prh9fD92z2z32xO2QYQtqBqrmve+nXlW9emOSOMqWHKk6kHU1+OAr6y0NHz8fIveCjyAgS7Mk/W25//m7z6xpPFeAxdvOvudDXHfhT7ByTBJKV9ksnjoBPNfFX+ctCNHO7rlfKcI/FH5E4Ue4MGLX/UwR3BNvfWZpF3+dI+Bj7oIMqc9+CABTQoiFI6kNzgNAJEgpUUkTgBSRUsRu/joDRBlBSQtAQpThwpwBVInPAtgp5gwQMM2MAImubNBpE24iAqiMgDUBLEFCHz+vTgBWT8Uffn1msO2yN/vZyhkpGlg1qepTJNY7Ndr7ZUn4BgAYK4O1McRv9w0OsDFSovJvljJ34YXTX2xPZhoR2Bi7V4pw/XziN+u6dQ2kQIwRpq+7xPW9y4PEskdmvS6Se3QnWRgDL7cC5GF8Mkp4P55aXX0lVoq3qMQYELOugTAzfNhbq482AEJMXNQhEtnNPqClXeOeNAB8sOpwzbU18BsAzpMJm/7NLWyGpIZm1pxe/Dv32+U+/4+j9nZjcAG9ZDCaCTDsH3sjd1fuD9GfFLIWIYGGEq0Hxcwi2FalNWUsZUnvx9sH97zWsGkryV799Mk787BjZrXXWmBm7LrNL6V4XysAdnV5cPfDLhShLi+JXrrA209fuvYfm6414YsfnfpBig+0Apj98f6z3x/v4q9zQZIXWF7AjG7vXFrvlN47vwVFMfuomUHuu/nrDuAgziAwAzdvgLy4MUCYd0WUO4ixPROYYRfOrXeqiTKAzAxKn8lUn4yZgAi7j73+4E/W50R5ECYYKl/KQt8N7aEkhaWDCWLtu97lpfIaZmYD4C5gCCwAvQourQDSCsKtHF++Y/XcsZfSxWRVkUBZp2YU+uvyJ1cvbv2+vWGlvYBQiQXAAw7IgS3gmpfGE4CMknpafAKwH41w4KQ/FU0H9NJyfHrVoQVi10v+0Imo2iayynrazsxYqBQA/CH9ds6Et7od+b/jfwHp+5qKBEXj3wAAAABJRU5ErkJggg==\" class=\"addButton\">&nbsp;&nbsp;&nbsp;<input type=\"image\" id=\"done\" name=\"done\" alt=\"I DIDit\" title=\"I DIDit\" onclick=\"return(shareList)\" src=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAK8AAACvABQqw0mAAAABh0RVh0U29mdHdhcmUAQWRvYmUgRmlyZXdvcmtzT7MfTgAABDBJREFUWIXdl2toHFUUx//n3tnd7MZuQmiCTSJqrLWuqKGQWiW2USGFFBKtMVW/+IAWjE2p1SqoqOAX/VCrTalEbX1B2igRWgW/iC2ipM07FmJtjU2QQpI1SbPZ18zchx+ySfeZhyQWO3CY3Z175ve795zZy5DWGlfzYFeVfs0LHGyj3KZ2Y/1cY2i5euBI963lDl7SwshRqLT5S8Tq3b2jzN/5nwh81rPBxymvLSqHvEKNwcmL4eSrtFSX3x0J/PzWK5u0uWwCn3T5rnfwmzrD9vkiIcfByAmlTXC2Am7HbZA68HXHX+11TTXT3CXtgddOEnFe0hqyhopMMQkNN6Rm0PDAVhYC0V8RsYerbi9YyWdyjKUUuCVny/tRe+S+qO0HsSxIpQHQFRQRSFPD7nv9cskFDndXP2bL4K6gdQmELEAhDg4QCIwcDbs2/PFpfN6S9MDHXVWFUqvfAtHfvRoKlKayBPbG3vKBt5N/z7gC77WVVWc7VtXbKnx25/of9s4lILXxxZR50SuUAlHqLRmxL18uv5ACBzI04YEzlY+7HcXHoyK0GXC9dKijuiUTvKnz0Z1he/yhiJiCghNSs4RQmneHdc4zmfJTStDYXvUEI2fzePg8bBUCgZDrXg0X935VX/bNtvixH3bV3miJYP9EZMDDKN1cKGiQ685XN/YNZhJIyDpw5pGNgKvZH7wASwoAHmi4MRYaRMSeqmts35qwEkKKI5PREY9UBKFYSmjt2D4XPEVgMjJ6/0hgAFFbQEoDQhCEIEjlxOjUIMJWsO6D01uPTcvWbp+KTjwYMkMJY2dzBD/6ZsXZY3PBgaQSvPj9mhKCcZpA+ekGS21jZfbNyHbl9UXtwFp/8E9X2o4nGmXkXvPO5o7JRQkAwAvf3eXTWp0CkFZCaYm87CKEzAlYMpL2kePMqN23pbd1PnhaAQBoOH63T2l1EkBBSgIAqQWIOBgIydlE7NuDNX3VC4EDGR7Dxpq+fimNB4Qgv5CE+LAlQSkHpGSwk64JyUJQWc8tFA7M80/4bEupT6nM5Ug+OOPPH97Wc2jJBADgyc9LfWqOnpi9Eaj96NN99ywGDixgO25+qrffsliFacJvmoBlpYZpQQvbsWOxcGARm9HDH61ba1viJxDyMbPLxlI5Y/tP1Pfu+TcCaTcjgwgxxExAaH2ucn/pJqXVKTAUQE1fIdAlaTtfJyKDX9GKn9XMdy3STJa01jCInAC8ADwAnAAcMTkGgMfOJIGJGyoK1hVX5O9jWbwYQltjPYE951qHfuRATjwsFgqAjJ0FABuABSAMICC0tuIFcgFkA3DF4EYcnM+shgRCnhVZ3sLKgjuCF8PDw91/D3HguhgkfvY6Di5jAgKACSAE4PKswDzLn1AKApgApNbaJiLGp4XjocmfEyK5DMv2XrDQ49p+NftfCPwDIKskFDb/Fv8AAAAASUVORK5CYII=\" class=\"addButton\"></p></form></div>" % (index, results[index].name, results[index].key())
                        
            if results[index].referringItem is not None:
                addedByHtml = ""
            else:
                countHtml = "<div class=\"count-bubble\"><a href=\"#\" alt=\"%s\" title=\"%s\">%s</a><div class=\"count-bubble-arrow-border\"></div><div class=\"count-bubble-arrow\"></div></div>" % (str(results[index].addedTotal) + " DOwhers", str(results[index].addedTotal) + " DOwhers", results[index].addedTotal)
                doneCountHtml = "<div class=\"count-bubble\"><a href=\"#\" alt=\"%s\" title=\"%s\">%s</a><div class=\"count-bubble-arrow-border\"></div><div class=\"count-bubble-arrow\"></div></div>" % (str(results[index].completedTotal) + " DID it!", str(results[index].completedTotal) + " DID it!", results[index].completedTotal)
                addedByHtml = "<div class=\"clear\"></div><div><a href=\"#\"><img class=\"thumb2\" src=\"%s\" alt=\"%s\" title=\"%s\" /></a></div>%s" % (u.profilePic, u.display_name, u.display_name, countHtml)
                scriptHtml += "\"%s\"," % (results[index].name.title())
            
            itemHtml = "<div class=\"grid_4\" style=\"padding:0;margin-left:0px;\"><div class=\"services_small_wrapper drop-shadow raised\">%s<div class=\"large2\"><a href=\"#\">%s</a></div><div class=\"float_left very_light\">%s</div>%s%s</div></div>" % (results[index].flickrImage, results[index].name.title(), results[index].location, addedByHtml, buttonHtml)
            
            ilist.append(itemHtml)
        
#        print(count)
    
        body_content = "Test"
        return render_to_response('layouts/index.html', glvars(locals(),globals()))

def test2(request):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)

    form = cgi.FieldStorage()
    if form.getvalue("value") is not None:
        search = form.getvalue("value")
    else :
        search = "dowhit"

    body_content = "Test"
    return render_to_response('layouts/indexOLD.html', glvars(locals(),globals()))

def start(request):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)

    if session.is_active():
        session.terminate()

    y=0
    m=0
    d=0

    if request.method == 'POST':
        u = MyUser()
        form = cgi.FieldStorage()
        if form.getvalue("dob") is not None:
            dob = datetime.datetime.strptime(form.getvalue("dob"),"%m/%d/%Y")
            u.dob = dob.date()
            session['me'] = u

        return redirect('/test', glvars(locals(),globals()))

    body_content = "Start"
    return render_to_response('layouts/start.html', glvars(locals(),globals()))

def token(request):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)

    # close any active session the user has since he is trying to login
    if session.is_active():
        session.terminate()

#    token = self.request.get('token')
    form = cgi.FieldStorage()
#    token = form.getvalue("connection_token")
    token = form.getvalue("token")

    api_params = {
        'token': token,
        'apiKey': '543f06aa3fab057d183b2cfdcabffb6dcba73bb7',
        'format': 'json',
    }
    
    http_response = urllib2.urlopen('https://rpxnow.com/api/v2/auth_info', urllib.urlencode(api_params))

    # read the json response
    auth_info_json = http_response.read()

    # Step 3) process the json response
    auth_info = json.loads(auth_info_json)

    # Step 4) use the response to sign the user in
    if auth_info['stat'] == 'ok':
        profile = auth_info['profile']

    # 'identifier' will always be in the payload
    # this is the unique idenfifier that you use to sign the user
    # in to your site
    
#    identifier = form.getvalue("UID")
        identifier = profile['identifier']
    
        u = MyUser()
        wl = WhitList()
        # these fields MAY be in the profile, but are not guaranteed. it
        # depends on the provider and their implementation.
    #    email = form.getvalue("email")
        try:
            email = profile['email']
        except KeyError:
            email = None
            
        try:
            #name = form.getvalue("nickname")
            name = profile['displayName']
    
        except KeyError:
            if email is not None:
                name = email.partition('@')[0]
            else:
                name = ""
            
#        if profile['photo'] is not None:
    #    if form.getvalue("photoURL") is not None:
        try:
            profile_pic_url = profile['photo']#form.getvalue("photoURL")
        except KeyError:
            profile_pic_url = "http://" + BASE_URL + "/static/images/avatar.png"
 #       else:
 #           profile_pic_url = "http://" + BASE_URL + "/static/images/avatar.png"
            #profile_pic_url = "http://www.dowhit.com/static/images/dowhitO.png"
    
        #default = "http://localhost:8081/static/images/dowhitO.png"
        # construct the url
        #gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        #gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
    
        try:
            #provider = form.getvalue("provider")
            provider = profile['providerName']
            provider = provider.lower()
        except KeyError:
            provider = ""
    
        if form.getvalue("gender") is not None:
            gender = form.getvalue("gender")
        else:
            try:
                gender = profile['gender']
                if gender == "m" or gender == "male":
                    gender = "Male"
                else:
                    if gender == "f" or gender == "female":
                        gender = "Female"
            except KeyError:
                gender = ""
    
        if provider == "facebook":
            try:
                #location = form.getvalue("city")
                location = profile['address']['formatted']
            except KeyError:
                location = ""
        else:
            location = ""
    
        ip = os.environ["HTTP_HOST"]
        response = urllib.urlopen('http://api.hostip.info/get_html.php?ip=%s' % ip).read()
        m = re.search('City: (.*)', response)
        if m:
            location = m.group(1)
        
#        if provider == "facebook" or provider == "google":
#            if profile['name'] is not None:
        try:
            #firstName = form.getvalue("firstName")
            firstName = profile['name']['givenName']
        except KeyError:
            firstName = ""
    
        try:
            #lastName = form.getvalue("lastName")
            lastName = profile['name']['familyName']
        except KeyError:
                lastName = ""
#            else:
#                firstName = ""
#                lastName = ""
        
        try:
            #profile_url = form.getvalue("profileURL")
            profile_url = profile['url']
        except KeyError:
            profile_url = None
            
        if form.getvalue("birthYear") is not None:
            dob = datetime.datetime.strptime(form.getvalue("birthMonth") + "/" + form.getvalue("birthDay") + "/" + form.getvalue("birthYear"),"%m/%d/%Y").date()
        else:
            try:
                dob = datetime.datetime.strptime(profile['birthday'],"%Y-%m-%d").date()
            except KeyError:
                dob = None    
    
        currentUser = u.get_or_insert(identifier, email=email, display_name=name, profilePic=profile_pic_url, provider=provider, gender=gender, firstName=firstName, lastName=lastName, profileURL=profile_url, location=location, dob=dob)
        key = currentUser.key()
    
        # get the user's record (ignore TransactionFailedError for the demo)
        session['me'] = currentUser
    
        wlIdentifier = identifier + "WhitList"
        wList = wl.get_or_insert(wlIdentifier, user=currentUser, name="Whit List")
        wlKey = wList.key()
    
        session['wl'] = wList
    
        created = currentUser.created
        now = datetime.datetime.now()
        
        if currentUser.authorized:
            #AUTHORIZED BETA USER
            if (now - datetime.timedelta(seconds=2)) > created:
                # RETURNING USER
                return redirect('/whitlist/', glvars(locals(),globals()))
            else:
                # NEW USER
                return redirect('/profile/', glvars(locals(),globals()))
        else:
            #NOT AUTHORIZED
            return redirect('/profile/', glvars(locals(), globals()))

    else:
        body_content = "Token"
        return redirect('/', glvars(locals(),globals()))
    return render_to_response('layouts/token.html', glvars(locals(),globals()))

def logout(request):
    session = get_current_session()
    if session.has_key('me'):
        session.terminate()

    return redirect('/', glvars(locals(),globals()))

#    return render_to_response('layouts/logout.html', glvars(locals(),globals()))

def sendmail(request):
    if request.method == 'POST':
        try:
            ref = os.environ['HTTP_REFERER']
        except KeyError:
            ref = "/test/"

        form = cgi.FieldStorage()
        user_address = form.getvalue("email")
        to_address = "feedback@dowhit.com"
        sender_address = "bpowell@primeight.com"
        subject = "DOwhit Feedback from %s" % (user_address)
        message = form.getvalue("message")
        environ = str(os.environ)
        environ = environ.replace(''', ''', ''', \n''')
        body = "%s \n \n \n \n Environment: \n %s" % (message,environ)

        mail.send_mail(sender_address, to_address, subject, body)

        return redirect(ref, glvars(locals(),globals()))
    
def profileajax(request):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)
    strdata = request.POST['data']
    dictdata = dict(item.split("=") for item in strdata.split("&"))
            
    currentUser.gender = dictdata['Gender']
    currentUser.ethnicity = urllib.unquote_plus(dictdata['Ethnicity'])
    currentUser.country = urllib.unquote_plus(dictdata['Country'])
    currentUser.location = dictdata['location']
    if dictdata['smoker'] is not None:
        if dictdata['smoker'] == "False":
            currentUser.smoker = False
        else:
            currentUser.smoker = True
    if dictdata['height'] <> 'None':
        if dictdata['weight'] <> 'None':
            ht = float(dictdata['height'])
            wt = float(dictdata['weight'])
            currentUser.height = int(ht)
            currentUser.weight = int(wt)
            currentUser.bmi = (wt / (ht**2)) * 703
            
    currentUser.display_name = urllib.unquote_plus(dictdata['display-name'])
    currentUser.email = urllib.unquote_plus(dictdata['email'])
    currentUser.firstName = urllib.unquote_plus(dictdata['first-name'])
    currentUser.lastName = urllib.unquote_plus(dictdata['last-name'])
    
    currentUser.dob = datetime.datetime.strptime(urllib2.unquote(dictdata['dob']),"%m/%d/%Y").date()

    try:
        if dictdata['emailaccount'] is not None:
            currentUser.emailAccount = True
    except KeyError:
        currentUser.emailAccount = False

    try:
        if dictdata['emailoffers'] is not None:
            currentUser.emailOffers = True
    except KeyError:
        currentUser.emailOffers = False    
    
    currentUser.put()

    session['me'] = currentUser
    
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)

    
    return render_to_response('layouts/ajax.html', glvars(locals(),globals()))

def profile(request):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)
    submit = "Update"
    
    if not currentUser:
        return redirect('/', glvars(locals(), globals()))

    if request.method == 'POST': # If the form has been submitted...
        #form = UserForm(request.POST) # A form bound to the POST data
        #if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
        #    u = MyUser.get_or_insert(identifier, email=email, display_name=name, profilePic=profile_pic_url, provider=provider, gender=gender, firstName=firstName, lastName=lastName, profileURL=profile_url, location=location)
        #    gender = form.cleaned_data['Gender']

        form = cgi.FieldStorage()
        currentUser.gender = form.getvalue("Gender")
        currentUser.display_name = form.getvalue("display-name")
        currentUser.email = form.getvalue("email")
        currentUser.firstName = form.getvalue("first-name")
        currentUser.lastName = form.getvalue("last-name")
        if form.getvalue("dob") is not None:
            dob = datetime.datetime.strptime(form.getvalue("dob"),"%m/%d/%Y")
            currentUser.dob = dob.date()
        else:
            currentUser.dob = None
        currentUser.emailAccount = form.getvalue("emailaccount")
        currentUser.emailOffers = form.getvalue("emailoffers")
        currentUser.ethnicity = form.getvalue("Ethnicity")
        currentUser.country = form.getvalue("Country")
        if form.getvalue("smoker") is not None:
            if form.getvalue("smoker") == "False":
                currentUser.smoker = False
            else:
                currentUser.smoker = True
        ht = float(form.getvalue("height"))
        wt = float(form.getvalue("weight"))
        currentUser.height = int(ht)
        currentUser.weight = int(wt)
        currentUser.bmi = (wt / (ht**2)) * 703
        currentUser.location = form.getvalue("location")

        currentUser.put()

        session['me'] = currentUser

        #return render_to_response('layouts/profile.html', glvars(locals(),globals()))
        return redirect('/whitlist', glvars(locals(),globals())) # Redirect after POST
    else:
        if request.GET:
            currentUser.agree = bool(request.GET['agree'])
            currentUser.put()
            session['me'] = currentUser
            return redirect('/whitlist/', glvars(locals(), globals()))
            
        if currentUser.authorized and not currentUser.agree:
            return redirect('/beta/', glvars(locals(), globals()))
            #return redirect('/thanks/', glvars(locals(), globals()))
        else:
            form = cgi.FieldStorage()
            #form['display-name'].value = currentUser.display_name
    
            if session.has_key('me'):
                userdisplay = currentUser.display_name
                email = currentUser.email
                name = currentUser.display_name
                profilePic = currentUser.profilePic
                provider = currentUser.provider
                firstName = currentUser.firstName
                lastName = currentUser.lastName
                profileURL = currentUser.profileURL
                if currentUser.dob is not None:
                    dob = datetime.date.strftime(currentUser.dob,"%m/%d/%Y")
                #dob = currentUser.dob
                emailAccount = currentUser.emailAccount
                emailOffers = currentUser.emailOffers
                gender = currentUser.gender
                ethnicity = currentUser.ethnicity
                country = currentUser.country
                state = currentUser.state
                zip = currentUser.zip
                smoker = currentUser.smoker
                height = str(currentUser.height)
                weight = str(currentUser.weight)
                outlook = currentUser.outlook
                location = currentUser.location
        #        bmi             = db.FloatProperty()
        #        BMI = ( Weight in Pounds / ( Height in inches x Height in inches ) ) x 703
        #        bp              = db.StringProperty()
        #        cholesterol     = db.IntegerProperty()

    body_content = "Profile"
    return render_to_response('layouts/profile.html', glvars(locals(),globals()))

def whitlist(request):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)
    submit = "Add"
    
    #names=[name for name in db.GqlQuery("SELECT * FROM WhitListItem")]
    #values={'names':','.join(names)}
    #request.response.out.write(template.render('list.html',values))

    names = ["Hike Grand Canyon","Death Valley see thermometer over 120","Learn to Fly Take flying lessons with the intent to get a pilot\'s license","Zipline (locally)","Climb or Hike Mt. Katadin, Maine","Ride in a hot air balloon","Go paragliding","Go parasailing in Acapulco","Go sky diving","Go on a helicopter ride","Go scuba diving","Go snorkeling in a shipwreck","Swim with sharks","Ride a mechanical bull","Climb Mount Kilimanjaro","Climb Mount Everest","Go fire walking","Go bungee jumping","Go white water rafting","Dive in a submarine","Fly in a blimp","Go rock climbing","Learn to fly a plane","Race a sports car","Fire a pistol","Go jet skiing","Take a canopy tour (traversing between trees on a zip line)","Go Zorbing in New Zealand","Ride the world\'s largest Ferris Wheels","Ride the 10 largest roller coasters in the world","Go on a cruise","Visit the wreckage of the Titanic aboard a submarine","Travel to the moon with Virgin Galactic","Experience weightlessness","Go on the world\'s top ten train rides","Watch a rocket launch, live","Break a Guinness World Record","Go on a cross-country motorcycle trip","Jump from a cliff into deep water","Swim in the largest swimming pool in the world, off the coast of Chile","Read One Book A Month","Learn conversational Spanish","Learn to say hello in 50 languages","Learn sign language","Learn Mandarin","Learn Latin","Choose a country and learn not only the language that is spoken there, but also study its customs, its cuisine, its art, and its history","Learn enough Italian to be able to understand opera","Learn your grandparents\' native tongue","Learn to play the piano","Take signing lessons","Learn to play the guitar","Learn to yodel","Compose a song","Release an album","Join the church choir","Learn to sing opera","Play in an orchestra","Conduct an orchestra","Form a band","Enroll in a music appreciation class","Sing Karaoke","Build a Jazz library","Build a classical music library","Make a list of 100 books you want to read","Read the complete works of Shakespeare","Read every novel that has won a Pulitzer Prize in the Fiction Category","Read all of the Russian classics","Read every book your favorite author has written","Read all of Agatha Christie\'s mystery novels","Visit the Bermuda Triangle","Be interviewed on Oprah","Be Time Magazine\'s Person of the Year","Be interviewed by Piers Morgan","Be listed as one of People Magazine\'s 50 Most Beautiful People","Be on the cover of \"Rolling Stone\" Magazine","Have a street named after you","Be one of CNN\'s Heroes (CNN\'s global search for everyday people changing the world)","Win a Nobel Prize","Receive a knighthood (or a damehood) from the Queen of England","Be elected to political office","Be inducted into a Hall of Fame","Be awarded a star on the Hollywood Walk of Fame","Cut the ribbon at a major opening","Win an Emmy","Make the front page of the newspaper","Be interviewed on The Today Show","Get an article published in The New Yorker","Get an article published in The Huffington Post","Write and publish a novel","Write a #1 New York Times\' Best Seller","Write an eBook","Win NaNoWriMo","Write a children\'s book","Write a cookbook","Write a play","Write a travel book","Write a textbook","Publish a book of poetry","Write for a TV sitcom","Write a comic book","Crack the Top 100 on Amazon Kindle","Earn enough from your writing to be able to quit your day job","Be recognized as an authority in your field","Be a world-renowned expert in your field","Be the best in the world in your field","Leave a valuable contribution in your area of expertise","Start your own business","Own a bar","Own a spa","Invent something","Invent a board game","Make a documentary film","Have your paintings exhibited in a gallery","Become a wild life photographer","Sell your original artwork","Become an interior designer","Become an architect","Design furniture","Be a clothes designer","Become a famous chef and open your own restaurant","Become a life coach","Become mayor of your city","Become governor of your state","Become a senator","Become an attorney","Become a judge","Become a dentist","Become a doctor","Become a nurse","Become a personal trainer","Become a yoga instructor","Become a college basketball coach","Become a professional athlete","Become an A-list Hollywood actor","Become a freelance writer","Become a stand-up comedian","Become a journalist","Become a newscaster","Become a teacher","Become a college professor","Create a web site","Start a blog (have it get to the Technorati top 1000)","Hit the front page of Digg","Create a YouTube video","Become a Giant Squid on Squidoo","Be highly influential on Social Media","Make a five-figure income from your online ventures","Sell My Photography Work online","Learn how to use a pogo stick","Learn to play chess","Learn to play poker (or bridge)","Learn to play pool","Take up photography","Learn to make pottery","Learn to sculpt","Take up astronomy","Learn astrology","Fly kites","Learn how to perform magic tricks","Make mobiles","Keep bees","Learn to juggle","Solve the Rubik\'s Cube","Build a village around a model train layout","Construct furniture","Do woodworking","Make stained glass windows","Learn to make candles","Make models of cars, ships or airplanes","Building doll houses","Learn to brew beer","Take up gourmet cooking","Paint - watercolors, oil, acrylics","Gardening","Grow prize-winning roses","Restore a classic car","Restore antiques","Learn to draw","Become a Wine Connoisseur","Become a Cheese Connoisseur","A rose covered gazebo in the backyard","A fireplace","A meditation room","A large kitchen with wooden floors","A breakfast nook","A herb garden","A sauna","A whirlpool bathtub","A home office","A canopy bed","A terrace","A pool","A well-stocked pantry","A guest bedroom","A skylight in the bedroom","A great room (living and dining room) with high ceilings and a grand piano","A wall mural in the hallway","A scented linen closet","A nursery","A library filled with leather-bound books","A tennis court","A fountain in the entrance","A wraparound porch","A man-cave in the basement","A yard with fruit trees","A grand staircase","A stable for horses","A fabulous view from the living room","A pond with Koi in the backyard","Grow bonsai trees","Grow orchids","Become a collector","Become a Wine Connoisseur","Ft Knox","Earn A College Degree","Finish high school","Get your GED","Get a college degree","Get a Masters","Get a PhD","Get into Med School","Pass the New York Bar","Get Certified as a Public Accountant","Get an MBA","Get Certified as a Financial Planner","Get into Harvard","Finish first in your class","Get into Juilliard","Shake hands with Al Gore","Meet Muhammad Ali","Meet your favorite Hollywood star","Meet the President of the United States","Meet Richard Branson","Meet Prince William (and/or Prince Harry)","Meet Bill Gates","Meet Donald Trump","Meet your favorite author","Meet Warren Buffet","Meet your childhood hero","Find the love of your life","Get married","Go on that honeymoon that keeps getting postponed","Have a child","Raise a happy and healthy child","Adopt a child","Create a home with an inviting, joyous, comfortable, loving atmosphere","Have a pet","Pass on a family heirloom to your child","Create a coat of arms for your family","Write a letter to each of your children telling them what you want them to know about your life and the lessons you\'ve learned","Donate to Charity","Volunteer","Make a difference in at least one person\'s life","Build a Habitat for Humanity Home","Volunteer at a soup kitchen","Join the Peace Corps","Donate a million dollars to a charity of your choice (anonymously or not)","Donate a million dollars to your alma mater","Make loans to entrepreneurs in developing countries through www.kiva.com","Join a Big Brother, Big Sister Program","Volunteer at a Homeless Shelter","Donate blood","Donate clothes you no longer use to a battered women\'s shelter","Donate children\'s books to a hospital near your home","Mentor someone at work","Go Green","Go WWOOFING","Have a happiness project","Release negative emotions and limiting beliefs","Allow yourself to make mistakes","Discover your life\'s purpose","Learn not to take what others do or say personally","Figure out your priorities","Learn to act within your sphere of influence and stop worrying about things which are not within your control","Become an early riser","Kick negative habits (smoking, overeating, watching too much television, and so on )","Attend one of Anthony Robbins\' weekend events","Go to one of Steve Pavlina\'s Weekend Workshops in Las Vegas","Become a better public speaker by joining Toastmasters","Learn to say NO without feeling guilty","Visit Ground Zero in NYC","Visit Vatican City","Meet the Dalai Lama and/or the Pope","Visit Tibet","Spend a week at a Silent Retreat","Experience bliss","Find inner peace","Learn to forgive","Do all the lessons in A Course in Miracles","Attend a Native American Sweat Lodge Ceremony","Become a Reiki Master","Heal your past","Learn to live in the now","Take up yoga","Take up tai chi","Take up Qi Gong","Have a past life regression","Learn to meditate","Go on an inner awakening retreat in India","Ride a Tour De France Stage","Visit All 30 MLB stadiums","Run a 10k","Run a half marathon","Run a marathon","Join the 50 States Marathon Club and run a marathon in all 50 states","Become a triathlete","Complete the Ironman Triathlon","Learn archery","Learn to play golf","Play golf with Jack Nicklaus","Go golfing at each of the 100 Best Major Golf Courses in the World","Join a bowling league","Swim across the English Channel","Learn to ski","Ski at the top ten ski resorts in the world","Go canoeing or kayaking","Take horseback riding lessons","Take up fishing (or fly fishing)","Learn how to ice skate","Learn how to figure skate","Learn how to roller blade","Learn to water ski","Learn to sail","Sail around the world","Learn to play tennis","Try fencing","Participate in the Tour de France","Learn to surf","Run with the bulls","Mush a Dog Sled","Watch turtles hatch and run for the ocean","Have an aquarium","Swim with dolphins","Go whale-watching","See penguins in their natural habitat","See a platypus","See a koala","Visit the San Diego Zoo","Go on safari","Save a species from extinction","Become a vegetarian","Adopt a pet from the animal shelter","Milk a cow","Join People for the Ethical Treatment of Animals (PETA)","Ride a camel in the Sahara desert","See gorillas in the wild in Uganda","Go bird watching in Costa Rica","An opera at the Scala of Milan","An Armani fashion show","A concert by your favorite entertainer","Carnegie Hall","A Broadway Play","A session of the US Supreme Court","The TED Talks","The Super Bowl","The Olympics","The World Cup","The Indianapolis 500-Mile Race","Wimbledon","The Kentucky Derby","Go To All Four Major Golf Tournaments: Masters, US Open, British Open, and PGA Championship","Throw Out the First Pitch at a Major League Baseball Game","Visit Mt. Rushmore","See Old Faithful in Yellowstone National Park","Travel to Ireland","Visit Plymouth Rock","Glouster MA Have a drink at the crows nest","Hot Air Balloon over Arizona desert","Own a Harley Davidson Motorcycle","Caribbean Cruise","Visit Texas","See Punxsutawney Phil","The Grand Canyon","Victoria Falls (between Zambia and Zimbabwe)","Iguassu Falls (between Brazil and Argentina)","The Great Barrier Reef","The Galapagos Archipelago","The Northern Lights (the Aurora Borealis)","The Fjords of Norway","The Amazon Rainforest","The Perito Moreno Glacier","The Dome of the Rock, Israel","Salzburg, Austria","Bora Bora","Karnak Temple Egypt","The Terracotta Warriors","Hong Kong Harbor","Mecca","Go on a pilgrimage to Santiago de Compostela","The Leaning Tower of Pisa","The Eiffel Tower","Dubrovnik, Croatia","The Panama Canal","Visit all 7 continents","Visit every country in the world","Live in a foreign country for six months","The Basilica di San Marco, Venice","St. Peter\'s Basilica, the Vatican, Rome","The Acropolis in Greece","The Alhambra in Spain","Gaudi\'s La Sagrada Familia, Barcelona, Spain","The Statues of Easter Island, Chile","Hagia Sophia, Turkey","Kiyomizu Temple in Japan","The Kremlin in Russia","The Pyramids of Giza, Egypt","Stonehenge, United Kingdom","The Sydney Opera House, Australia","The Big Ben and the Houses of Parliament, London, England","The Parthenon in Greece","Machu Picchu, Peru","The Coliseum in Rome","Petra, Jordan","Christ Redeemer, Brazil","The Great Wall of China","Chichen Itza, Mexico","The Taj Mahal, India","Notre Dame Cathedral, Paris","See the Golden Gate Bridge in San Francisco","Go to the Pike Place Market in Seattle","See Mount Rushmore","See the Empire State Building","Climb up the Statue of Liberty","Go to Faneuil Hall Marketplace, Boston, MA","Visit SeaWorld Florida, Orlando","Go to Universal Studios, Hollywood, CA","Visit Waikiki Beach, Oahu, Hawaii","Visit Disney World","Visit all Fifty of the United States","See the Radio City Christmas Spectacular","Be invited to the Playboy Mansion\'s annual Halloween Party","Go to a St. Patrick\'s Day Parade","Go to the White House Easter Egg Roll","Go to the Macy\'s Thanksgiving Day Parade","Go to Times Square on New Year\'s Eve","Buy A Lake House","Pay off My Mortgage","Shop at Harrods","Charter a yacht","Own a beach house","Own a private jet","Vacation at Martha\'s Vineyard","Spend a week at a 5-star spa","Shop in Rodeo Drive","Go to an auction at Christie\'s or Sotheby\'s","Have High Tea at the Plaza Hotel in New York, or perhaps at Fortnum & Mason in London","Own a Rolls Royce, an Aston Martin, or a Bentley","Become an art collector","Gamble at Monte Carlo, Monaco","Drive a Lamborghini or a Ferrari","Sleep in a castle","Own an island","Become financially literate","Create a financial strategy","Invest in the stock market","Create enough passive income so that you don\'t have to work another day in your life","Create a trust fund for your child","Create a corporation to protect your assets","Open a Swiss bank account"]
    test = ["aaaaaa", "bbbbbb", "cccccc", "dddddd", "eeeeee"]
        
    if request.GET:
        newItem = request.GET['Item']
    
    if not currentUser:
        return redirect('/', glvars(locals(), globals()))

    if not currentUser.authorized:
        return redirect('/profile/', glvars(locals(), globals()))
    else:
        if not currentUser.agree:
            return redirect('/beta/', glvars(locals(), globals()))
            
        if session.has_key('wl'):
            wList = WhitList()
            wList = session['wl']

#        wli = WhitListItem()
#        liLink = WhitItemLink()
#        wListItem = wli.get_or_insert("Finish My Whit List", whitList=wList, name="Finish My Whit List", desc="This is your first whit list item.  This is an example item to show you what is possible with this list.", status="open")
#        wListItemLink = liLink.get_or_insert("http://en.wikipedia.org/wiki/Stonehenge", item=wListItem, link="http://en.wikipedia.org/wiki/Stonehenge")
#        wListItemLink = liLink.get_or_insert("http://maps.google.com/maps/place?rlz=1C1GGLS_enUS366US366&um=1&ie=UTF-8&q=stonehenge&fb=1&gl=us&hq=stonehenge&hnear=stonehenge&cid=13565595783028833449&pcsi=13565595783028833449,1", item=wListItem, link="http://maps.google.com/maps/place?rlz=1C1GGLS_enUS366US366&um=1&ie=UTF-8&q=stonehenge&fb=1&gl=us&hq=stonehenge&hnear=stonehenge&cid=13565595783028833449&pcsi=13565595783028833449,1")
#
#        session['wl'] = wList

#    whitList        = db.ReferenceProperty(WhitList, collection_name='whitListItems')
#    name            = db.StringProperty()
#    desc            = db.TextProperty()
#    tag             = db.ListProperty(unicode,default=['Adventure','Career','Community','Culture & Arts','Education','Entertainment','Family','Fitness','Health & Wellness','Hobbies','Home Improvement','Issues & Causes','Literature','Music','Outdoor Recreation','Relationships','Spiritual','Sports','Travel','Wealth & Finance'])
#    date            = db.DateTimeProperty()
#    rank            = db.RatingProperty()
#    cost            = db.FloatProperty()
#    status          = db.StringProperty(choices=('open', 'completed'))
#    private         = db.BooleanProperty(default=False)

    #wlist = ("Test Item", "Witness something truly majestic", "Help a complete stranger for the good", "Laugh till I cry", "Drive a Shelby Mustang", "Kiss the most beautiful girl in the world", "Get a tattoo", "Skydiving", "Visit Stonehenge", "Spend a week at the Louvre", "See Rome", "Dinner at La Chevre d'Or", "See the Pyramids", "Get back in touch", "Visit the Taj Mahal", "Hong Kong", "Victoria Falls", "Go on a safari", "Drive a motorcycle on the Great Wall of China", "Sit on the Great Egyptian Pyramids", "Find the Joy in your life")

    body_content = "whitList"
    return render_to_response('layouts/whitlist.html', glvars(locals(),globals()))

def newitem(request):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)

    if request.method == 'POST': # If the form has been submitted...
        #form = UserForm(request.POST) # A form bound to the POST data
        #if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
        #    u = MyUser.get_or_insert(identifier, email=email, display_name=name, profilePic=profile_pic_url, provider=provider, gender=gender, firstName=firstName, lastName=lastName, profileURL=profile_url, location=location)
        #    gender = form.cleaned_data['Gender']


        if session.has_key('wl'):
            wList = WhitList()
            wList = session['wl']
            
            form = cgi.FieldStorage()
            name = form.getvalue("newName")
            if form.getvalue("done.x") is not None:
                stat = "completed"
            else:
                stat="open"
                
            refer = None
            desc = ""
            tag = []
            flickrImage = ""
            location = ""
                
            if form.getvalue("newItem") is not None:
                refer = form.getvalue("newItem")
                rli = WhitListItem()
                rListItem = rli.get(refer)
                
                go = True
                for item in wList.whitListItems:
                    if item.name.upper() == rListItem.name.upper():
                        go = False
                
                if go:
                    rListItem.addedTotal += 1
                    rListItem.put()
                    desc = rListItem.desc
                    tag = rListItem.tag
                    flickrImage = rListItem.flickrImage
                    location = rListItem.location
    
            wli = WhitListItem()
            ident = name + str(wList.key())
            wListItem = wli.get_or_insert(ident, whitList=wList, name=name, status=stat, desc=desc, tag=tag, flickrImage=flickrImage, location=location, referringItem=refer)
            session['wl'] = wList
            
            if stat=="completed":
                wListItem.status = stat
                wListItem.accomplishDate = datetime.date.today()
                wListItem.put()
                rListItem.completedTotal += 1
                rListItem.put()
                    
            #return render_to_response('layouts/profile.html', glvars(locals(),globals()))
            #return redirect('/list/?Item=' + name, glvars(locals(),globals())) # Redirect after POST
            return redirect('/whitlist/?Item=' + name, glvars(locals(),globals())) # Redirect after POST
        else:
            return redirect('/', glvars(locals(),globals())) # Redirect after POST
    else:
        return redirect('/', glvars(locals(),globals())) # Redirect after POST

def saveitem(request):
    profileLink, logLink, session, currentUser, countdown_date, y, m, d, h, mn, s, adjDays = getSessionUser(request)

    if request.method == 'POST': # If the form has been submitted...
        #form = UserForm(request.POST) # A form bound to the POST data
        #if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
        #    u = MyUser.get_or_insert(identifier, email=email, display_name=name, profilePic=profile_pic_url, provider=provider, gender=gender, firstName=firstName, lastName=lastName, profileURL=profile_url, location=location)
        #    gender = form.cleaned_data['Gender']

        form = cgi.FieldStorage()
        if form.getvalue("submit") is not None:
            key = form.getvalue("submitvalue")
            name = form.getvalue("name")
            desc = form.getvalue("desc")

            wli = WhitListItem()
            wli = db.get(key)

            if form.getvalue("sort") is not None:
                priority = int(form.getvalue("sort"))
            else:
                priority = None

            if form.getvalue("private") is not None:
                if form.getvalue("private") == "False":
                    private = False
                else:
                    private = True

            if form.getvalue("accomplishBy") is not None:
                if form.getvalue("accomplishBy") == "":
                    wli.accomplishBy = None
                else:
                    accomplishBy = datetime.datetime.strptime(form.getvalue("accomplishBy"),"%m/%d/%Y")
                    wli.accomplishBy = accomplishBy.date()
            else:
                wli.accomplishBy = None

            if form.getvalue("accomplishDate") is not None:
                if form.getvalue("accomplishDate") == "":
                    wli.accomplishDate = None
                else:
                    accomplishDate = datetime.datetime.strptime(form.getvalue("accomplishDate"),"%m/%d/%Y")
                    wli.accomplishDate = accomplishDate.date()
                    wli.status = "completed"
            else:
                wli.accomplishDate = None
                wli.status = "open"

            if form.getvalue("tags") is not None:
                taglist = []
                if type(form.getvalue("tags")) is str:
                    taglist.append((form.getvalue("tags")))
                else:
                    taglist = form.getvalue("tags")

                wli.tag = taglist

            wli.sortOrder = priority
            wli.name = name
            wli.desc = desc
            wli.private = private
            wli.put()

            session["wl"] = wli.whitList

        elif form.getvalue("del") is not None:
            key = form.getvalue("del")
            wli = WhitListItem()
            wli = db.get(key)
            db.delete(wli.links.fetch(10))
            db.delete(wli.pics.fetch(100))
            db.delete(wli.comments.fetch(100))
            db.delete(wli)


#        if session.has_key('wl'):
#            wList = WhitList()
#            wList = session['wl']
#
#            wli = WhitListItem()
#            wListItem = wli.get_or_insert(name, whitList=wList, name=name, status="open", desc="")
#            session['wl'] = wList
        #return render_to_response('layouts/list.html', glvars(locals(),globals()))
        return redirect('/whitlist/', glvars(locals(),globals())) # Redirect after POST
#        else:
#            return redirect('/test/', glvars(locals(),globals())) # Redirect after POST
    else:
        return redirect('/test/', glvars(locals(),globals())) # Redirect after POST