#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import os
import urllib

import jinja2
import webapp2
from google.appengine.ext import db
from google.appengine.api import users
import string
import random
import counter
import security
import idea



JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True

)


class Investor(db.Model):
    createDate = db.DateTimeProperty(auto_now_add = True)
    investmentGroup = db.StringProperty()
    loseFunds = db.FloatProperty()

class Transaction(db.Model):
    amount = db.FloatProperty
    moneySync = db.StringProperty()
    investmentGroup = db.StringProperty()
    securityToken = db.StringProperty()

class Project(db.Model):
    name = db.StringProperty()
    moneyNeeded = db.FloatProperty()
    moneyRecieved = db.FloatProperty()

class VoteType(db.Model):
    name = db.StringProperty()
    text = db.TextProperty()
    value1C = db.IntegerProperty()
    value1P = db.IntegerProperty()
    value2C = db.IntegerProperty()
    value2P = db.IntegerProperty()
    value3C = db.IntegerProperty()
    value3P = db.IntegerProperty()
    value4C = db.IntegerProperty()
    value4P = db.IntegerProperty()

class Vote(db.Model):
    value = db.IntegerProperty()
    user = db.UserProperty()
    capitalist = db.BooleanProperty()








#class BoardOfDirectors
#    createDate = db.DateTimeProperty(auto_now_add = True)
#    googleID = db.UserProperty()
    


#class InvestmentGroups
#    createDate = db.DateTimeProperty(auto_now_add = True)
#    name = db.StringProperty()
#    website = db.StringProperty()
#    moto = db.StringProperty()
#    image = db.StringProperty()
#    voteControl = db.BooleanProperty()
#    profitControl = db.BooleanProperty()



class Application(db.Model):
    createDate = db.DateTimeProperty(auto_now_add = True)
    tfycID = db.StringProperty()
    claimed = db.BooleanProperty()
    invest = db.IntegerProperty()
    googleID = db.UserProperty()
    

class Investor(db.Model):
    createDate = db.DateTimeProperty(auto_now_add = True)
    googleID = db.UserProperty()
    tfycID = db.StringProperty()
    invest = db.IntegerProperty()
    InvestmentGroups = db.IntegerProperty()

def Application_key(a_key=None):
    return db.Key.from_path('Application', a_key or 'default_key')

def Investor_Key(a_key=None):
    return db.Key.from_path('Investor', a_key or 'default_key')


def id_generator(size=40, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def signInCheck():
    return True

#class CreateInvestorGroup(webapp2.RequestHandler):
#    def get(self):


class CreateID(webapp2.RequestHandler):
    def get(self):
       money = self.request.get('Money')
       if (money==""):
         self.response.out.write('Money')
         return
       money = int(money)
       tfycID = id_generator()
       saveData = Application(key=Application_key(tfycID))
       saveData.tfycID = tfycID
       saveData.claimed = False
       saveData.invest = money
       saveData.put()
       self.response.out.write(tfycID)

class RedeemID(webapp2.RequestHandler):
    def get(self):
        id = self.request.get('ID')
        if (id==""):
          self.response.out.write("No ID")
          return
        application = Application.get_by_key_name (id)
        if (application==None):
          self.response.out.write("Not Yet Setup")
          return
        if (application.claimed):
          self.response.out.write("ID Already Used")
          return
        user = users.get_current_user()
        if user:
            application.claimed=True
            application.googleID=user
            invest = Investor(key=Investor_Key(user.user_id()))
            invest.googleID=user
            invest.tfycID = id
            invest.invest = application.invest
            invest.clan = 0
            invest.put()
            self.response.out.write("ID Assoicated with your Google Account")      
        else:
          url = '/RedeemID?ID=id' 
          greeting = ('<a href="%s">Sign in or register</a>.' % users.create_login_url(url))
          self.response.out.write("<html><body>%s</body></html>" % greeting)
          
class Profile(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
          user = users.get_current_user()
        else:
          url = '/Profile' 
          greeting = ('<a href="%s">Sign in or register</a>.' % users.create_login_url(url))
          self.response.out.write("<html><body>%s</body></html>" % greeting)

          
        
class MainHandler(webapp2.RequestHandler):
    def get(self):       
        template = JINJA_ENVIRONMENT.get_template('holding.jinja')
        self.response.out.write(template.render())
        
class TestDisplay(webapp2.RequestHandler):
    def get(self):       
        template = JINJA_ENVIRONMENT.get_template('main.jinja')
        self.response.out.write(template.render())       

class FrontPage1(webapp2.RequestHandler):
    def get(self):       
        self.response.out.write("Page 1")  

class FrontPage2(webapp2.RequestHandler):
    def get(self):       
        self.response.out.write("Page 1") 
          


class Youtube(webapp2.RequestHandler):
    def get(self):       
        self.response.out.write('''<meta http-equiv="refresh" content="0; url=http://www.youtube.com/channel/UChwoDCOjliin3x0Y_ShiGGw" />''')

class rulesWIVG(webapp2.RequestHandler):
    def get(self):       
        self.response.out.write('''<meta http-equiv="refresh" content="0; url=https://docs.google.com/document/d/1YUbA6KMjBF3iRNklWHady_CzOADW4604Q1Ut1DHEdIw/edit?usp=sharing" />''')

class faqWIVG(webapp2.RequestHandler):
    def get(self):       
        self.response.out.write('''<meta http-equiv="refresh" content="0; url=https://docs.google.com/document/d/1_JYfc6oAtvEB-yFPUQZBUiZzcAFOkT0PiVjPWkj7i4s/edit?usp=sharing" />''')
		
		
		

class FormHandler(webapp2.RequestHandler):
    def get(self):       
        template = JINJA_ENVIRONMENT.get_template('info.jinja')
        self.response.out.write(template.render())

class Login(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ('Welcome, -%s-! (<a href="%s">sign out</a>)' %
                        (user.user_id(), users.create_logout_url('/Login')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/Login'))

        self.response.out.write("<html><body>%s</body></html>" % greeting)


class questionPeriodsWIVG(webapp2.RequestHandler):
    def get(self):       
        template = JINJA_ENVIRONMENT.get_template('eventList.jinja')
        self.response.out.write(template.render())

class submitWIVG(webapp2.RequestHandler):
    def get(self):       
        template = JINJA_ENVIRONMENT.get_template('submit.jinja')
        self.response.out.write(template.render())

class signout(webapp2.RequestHandler):
    def get(self):
        greeting = ('Go Away! (<a href="%s">sign out</a>)' %
                    (users.create_logout_url('/Login')))
        self.response.out.write("<html><body>%s</body></html>" % greeting)

app = webapp2.WSGIApplication([
    ('/', TestDisplay),
    ('/TestDisplay', TestDisplay),
    ('/FrontPage1', FrontPage1),
    ('/FrontPage2', FrontPage2),
    ('/Apply', FormHandler),
    ('/CreateID', CreateID),
    ('/RedeemID', RedeemID),
    ('/Login', Login),
    ('/Youtube', Youtube),
    ('/questionPeriodsWIVG', questionPeriodsWIVG),
    ('/faqWIVG', faqWIVG),
    ('/rulesWIVG', rulesWIVG),
    ('/submitWIVG', submitWIVG),
    ('/submitIdea', idea.submitIdea),
    ('/viewIdea', idea.viewIdea),
    ('/generateSecurity', security.generateCode),
    ('/redeemSecurity', security.redeemCode),
    ('/signout', signout)
], debug=True)
