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





JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True

)



class CodeGenerator(db.Model):
    level = db.IntegerProperty()
    redeemed = db.BooleanProperty()

def CodeGenerator_key(a_key=None):
    return db.Key.from_path('CodeGenerator', a_key or 'default_key')

class SecurityLevel(db.Model):
    createDate = db.DateTimeProperty(auto_now_add = True)
    user = db.UserProperty()
    email = db.StringProperty()
    level = db.IntegerProperty()

def SecurityLevel_key(a_key=None):
    return db.Key.from_path('SecurityLevel', a_key or 'default_key')


def checkSecurityLevel(user=None):
    if (user==None):
        return 0
    level = SecurityLevel.get(SecurityLevel_key(user.user_id()))
    if level:
        return level.level
    return 0


def id_generator(size=40, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))



class generateCode(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if checkSecurityLevel(user) > 5:
                template = JINJA_ENVIRONMENT.get_template('createCode.jinja')
                self.response.out.write(template.render())
            else:
                q = SecurityLevel.all()
                count = 0
                for p in q.run(limit=1):
                    count = 1
                if (count == 1):
                    self.response.out.write("User Security Not High Enough")
                else:
                    newID = SecurityLevel(key=SecurityLevel_key(user.user_id()))
                    newID.user = user;
                    newID.email = user.email()
                    newID.level = 9001
                    newID.put()
                    self.response.out.write("Your Level is over 9000")
                    
        else:
            url = '/generateSecurity'
            self.response.out.write('''<meta http-equiv="refresh" content="0; url=%s" />''' % users.create_login_url(url));
    def post(self):
        user = users.get_current_user()
        if user:
            userLevel = checkSecurityLevel(user)
            if userLevel > 5:
                newLevel=self.request.get('nameLevel')
                newLevel = int(newLevel)
                if newLevel < userLevel:
                    newString = id_generator()
                    newID = CodeGenerator(key=CodeGenerator_key(newString))
                    newID.level = newLevel
                    newID.redeemed = False;
                    newID.put()
                    self.response.out.write('''<meta http-equiv="refresh" content="0; url=/redeemSecurity?redeemCode=%s" />''' % newString);



class redeemCode(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            redeemCode = self.request.get('redeemCode')
            code = CodeGenerator.get(CodeGenerator_key(redeemCode))
            if code:
                userLevel = checkSecurityLevel(user)
                if userLevel > code.level:
                    self.response.out.write("Send This Link to the Person you wish to Add")
                else:
                    if code.redeemed == False:
                        newID = SecurityLevel(key=SecurityLevel_key(user.user_id()))
                        newID.user = user;
                        newID.email = user.email()
                        newID.level = code.level
                        newID.put()
                        code.redeemed = True
                        code.put()
                        self.response.out.write("User Granted Level %s" % newID.level)
                    else:
                        self.response.write.out("This Code hass been redeemed")
            else:
                self.response.out.write("This code has not been created")
        else:
            url = '/redeemSecurity'
            self.response.out.write('''<meta http-equiv="refresh" content="0; url=%s" />''' % users.create_login_url(url));





