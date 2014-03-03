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




JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True

)


class Idea_VideoGameW1(db.Model):
    createDate = db.DateTimeProperty(auto_now_add = True)
    name = db.StringProperty()
    tagline = db.StringProperty()
    genres = db.StringProperty()
    describe = db.TextProperty()
    original = db.TextProperty()
    look =db.TextProperty()
    who = db.TextProperty()
    email = db.StringProperty()
    additionalInfo = db.TextProperty()
    residenceStatus = db.TextProperty()
    legal1 = db.BooleanProperty()
    legal2 = db.BooleanProperty()
    legal3 = db.BooleanProperty()
    visible = db.BooleanProperty()
    review = db.BooleanProperty()
    comment = db.BooleanProperty()

def Idea_VideoGameW1_key(a_key=None):
    return db.Key.from_path('Idea_VideoGameW1', a_key or 'default_key')

def Idea_QuickGet_key(a_key=None):
    return db.Key.from_path('Idea_QuickGet', a_key or 'default_key')

class Idea_QuickGet(db.Model):
    link = db.ReferenceProperty(Idea_VideoGameW1)

class submitIdea(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            submission =  Idea_VideoGameW1.get(Idea_VideoGameW1_key(user.user_id()))
            template = JINJA_ENVIRONMENT.get_template('ideaWIVG.jinja')
            if (submission==None):
                counter.increment('IdeaWIVG1')
                
                submission = Idea_VideoGameW1(key=Idea_VideoGameW1_key(user.user_id()))
                submission.put()
                quickGet = Idea_QuickGet(key=Idea_QuickGet_key(counter.get_count('IdeaWIVG1')))
                quickGet.link = submission
                quickGet.put()
            
            a = ''
            b = ''
            c = ''
            d = ''
            e = ''
            f = ''
            z = False
            if submission.legal1:
                a='checked'
            if submission.legal2:
                b='checked'
            if submission.legal3:
                c='checked'
            if submission.review:
                d='checked'
            if submission.comment:
                e='checked'
            if submission.visible:
                f='checked'
            template_values = {
            "name": submission.name,
            "tagline": submission.tagline,
            "genres": submission.genres,
            "describe": submission.describe,
            "original": submission.original,
            "look": submission.look,
            "who": submission.who,
            "email": submission.email,
            "additionalInfo": submission.additionalInfo,
            "residenceStatus": submission.residenceStatus,
            "legal1": a,
            "legal2": b,
            "legal3": c,
            "review": d,
            "comment": e,
            "showIt": f,
            "justSaved":z 
            }
            
            
            self.response.out.write(template.render(template_values))
        
        else:
            url = '/submitIdea'
            self.response.out.write('''<meta http-equiv="refresh" content="0; url=%s" />''' % users.create_login_url(url));
    def post(self):
        user = users.get_current_user()
        if user:
            submission =  Idea_VideoGameW1.get(Idea_VideoGameW1_key(user.user_id()))
            if (submission==None):
                counter.increment('IdeaWIVG1')
                submission = Idea_VideoGameW1(key=Idea_VideoGameW1_key(user.user_id()))
                submission.put()
                quickGet = Idea_QuickGet(key=Idea_QuickGet_key(counter.get_count('IdeaWIVG1')))
                quickGet.link = submission
                quickGet.put()
            submission.name=self.request.get('name')
            submission.tagline=self.request.get('tagline')
            submission.genres=self.request.get('genres')
            
            submission.describe=self.request.get('describe')
            submission.original=self.request.get('original')
            submission.look=self.request.get('look')
            
            submission.who=self.request.get('who')
            submission.email=self.request.get('email')
            submission.additionalInfo=self.request.get('additionalInfo')
            
            
            submission.residenceStatus=self.request.get('residenceStatus')
            submission.legal1=False;
            submission.legal2=False;
            submission.legal3=False;
            submission.review = False;
            submission.comment = False;
            submission.visible = False;
            
            a = ''
            b = ''
            c = ''
            d = ''
            e = ''
            f = ''
            z = True
            
            
            
            if self.request.get('legal1'):
                submission.legal1 = True;
                a = 'checked'
            if self.request.get('legal2'):
                b = 'checked'
                submission.legal2 = True;
            if self.request.get('legal3'):
                c = 'checked'
                submission.legal3 = True;
            if self.request.get('review'):
                d = 'checked'
                submission.review = True;
            if self.request.get('comment'):
                e = 'checked'
                submission.comment = True;
            if self.request.get('showIt'):
                f = 'checked'
                submission.visible = True

            
            

            
            
            submission.put()
            template = JINJA_ENVIRONMENT.get_template('ideaWIVG.jinja')
           

            template_values = {
            "name": submission.name,
            "tagline": submission.tagline,
            "genres": submission.genres,
            "describe": submission.describe,
            "original": submission.original,
            "look": submission.look,
            "who": submission.who,
            "email": submission.email,
            "additionalInfo": submission.additionalInfo,
            "residenceStatus": submission.residenceStatus,
            "legal1": a,
            "legal2": b,
            "legal3": c,
            "review": d,
            "comment": e,
            "showIt": f,
            "justSaved":z 

            }
            self.response.out.write(template.render(template_values))


class viewIdea(webapp2.RequestHandler):
    def get(self):
        id = self.request.get('id')
        if id:
            id = int(id)
            
            maxID= counter.get_count('IdeaWIVG1')
            quickLink =  Idea_QuickGet.get(Idea_QuickGet_key(id))
            while not quickLink and id < maxID:
                id = id +1
                quickLink =  Idea_QuickGet.get(Idea_QuickGet_key(id))
                
                if (quickLink):
                    submission = quickLink.link
                    if submission.visible is False:
                        quickLink=0
            if id >=maxID+1:
                id=1
                quickLink =  Idea_QuickGet.get(Idea_QuickGet_key(id))
            next = id+1
            if (next>maxID):
                next=1
            past = id-1
            if (id==1):
                past=maxID
            if quickLink:
                template = JINJA_ENVIRONMENT.get_template('viewIdeaWIVG.jinja')
                submission = quickLink.link
                comment = 'false'
                if submission.comment:
                    comment = 'true'
                
                template_values = {
                "name": submission.name,
                "tagline": submission.tagline,
                "genres": submission.genres,
                "describe": submission.describe,
                "original": submission.original,
                "look": submission.look,
                "who": submission.who,
                "email": submission.email,
                "additionalInfo": submission.additionalInfo,
                "next":next,
                "past":past,
                "current":id,
                "comment":comment
                }
                if submission.visible is True:
                    self.response.out.write(template.render(template_values))
                else:
                    self.response.out.write('Not Visible')
            else:
                template = JINJA_ENVIRONMENT.get_template('404.jinja')
                self.response.out.write(template.render())
    
        
        
        
        else:
            template = JINJA_ENVIRONMENT.get_template('404.jinja')
            self.response.out.write(template.render())