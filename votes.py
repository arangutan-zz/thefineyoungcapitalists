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
import counter
import Cookie
import datetime


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

class VoteEmpower(db.Model):
   createDate = db.DateTimeProperty(auto_now_add = True)
   email = db.StringProperty()
   voteSelected = db.IntegerProperty()


def VoteEmpower_key(a_key=None):
    return db.Key.from_path('VoteEmpower', a_key or 'default_key')



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

class votingEmpowered(webapp2.RequestHandler):
    def get(self):
        template_values = {
            "voteValue": 0
        }
        template = JINJA_ENVIRONMENT.get_template('main2.jinja')
        self.response.out.write(template.render(template_values))

class votingEmpoweredGrab(webapp2.RequestHandler):
    def get(self):
        value = int(self.request.get('id'))
        cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
        voteNumber = 0;
        if cookie:
            if "LastVote" in cookie:
                if int(cookie["LastVote"].value) != 0:
                    voteNumber = int(cookie["LastVote"].value);
                    stringOfCounter = 'IdeaWIVG_' + str(value);
                    stringOfCounterD = 'IdeaWIVG_' + str(voteNumber) + 'D';
                    counter.increment(stringOfCounter)
                    counter.increment(stringOfCounterD)
                else:
                    stringOfCounter = 'IdeaWIVG_' + str(value);
                    counter.increment(stringOfCounter)
            else:
                stringOfCounter = 'IdeaWIVG_' + str(value);
                counter.increment(stringOfCounter)
        NameOfVoted = "";
        if (value ==1):
            NameOfVoted  = "My Eyes"
        elif (value ==2):
            NameOfVoted  = "Furball Fury"
        elif (value ==3):
            NameOfVoted  = "Lux"
        elif (value ==4):
            NameOfVoted  = "Air Rocky"
        elif (value ==5):
            NameOfVoted  =  "Afterlife Empire"
        template = JINJA_ENVIRONMENT.get_template('WIVGVote.jinja')
        template_values = {
            "voteName": NameOfVoted,
            "voteValue": value,
            "Amount1":counter.get_count('IdeaWIVG_1')-counter.get_count('IdeaWIVG_1D'),
            "Amount2":counter.get_count('IdeaWIVG_2')-counter.get_count('IdeaWIVG_2D'),
            "Amount3":counter.get_count('IdeaWIVG_3')-counter.get_count('IdeaWIVG_3D'),
            "Amount4":counter.get_count('IdeaWIVG_4')-counter.get_count('IdeaWIVG_4D'),
            "Amount5":counter.get_count('IdeaWIVG_5')-counter.get_count('IdeaWIVG_5D'),
        }
        self.response.out.write(template.render(template_values))



class votingEmpoweredGrabX(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            vote =  VoteEmpower.get(VoteEmpower_key(user.user_id()))
            if (vote==None):
                vote = VoteEmpower(key=VoteEmpower_key(user.user_id()))
            vote.email=user.email();
            vote.voteSelected=int(self.request.get('id'));
            vote.put();
            template_values = {
                "voteValue": vote.voteSelected
            }
            template = JINJA_ENVIRONMENT.get_template('main2.jinja')
            self.response.out.write(template.render(template_values))

        else:
            url = '/VoteEmpowered?id='+self.request.get('id')
            self.response.out.write('''<meta http-equiv="refresh" content="0; url=%s" />''' % users.create_login_url(url));


