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
import project





JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True

)


class VoteType(db.Model):
    name = db.StringProperty()
    text = db.TextProperty()

class Vote(db.Model):
    value = db.IntegerProperty()
    user = db.UserProperty()
    capitalist = db.BooleanProperty()

def VoteType_key(a_key=None):
    return db.Key.from_path('CodeGenerator', a_key or 'default_key')

def Vote_key(a_key=None):
    return db.Key.from_path('CodeGenerator', a_key or 'default_key')




class createNewVoteType(webapp2.RequestHandler):
    def post(self):
        voteName = self.request.get('voteName')
        name = self.request.get('name')
        text = self.request.get('text')
        user = users.get_current_user()
        if user:
            userLevel = checkSecurityLevel(user)
            if userLevel > 9:
                projectCode = self.request.get('projectCode')
                project = project.Project.get(projectCode)
                if project:
                    newVoteType = VoteType(key=VoteType_key(project.name+voteName))
                    newVoteType.name = name
                    newVoteType.text = text
                    self.response.out.write(project.name+voteName)
                else:
                    self.response.out.write("Project Does Not Exist")
            else:
                self.response.out.write("Your Security Level Is Not High Enough")
        else:
            url = '/redeemSecurity'
            self.response.out.write('''<meta http-equiv="refresh" content="0; url=%s" />''' % users.create_login_url(url));

class createVote(webapp2.RequestHandler):
    def get(self):
        id = self.request.get('id')
        voteType = VoteType.get(id)
        if voteType:
            user = users.get_current_user()
            if user:
                userLevel = checkSecurityLevel(user)
                if userLevel>0:
                    Vote(key=Vote_key("a"))





