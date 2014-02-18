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
import security




JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True

)

class Project(db.Model):
    name = db.StringProperty()
    moneyNeeded = db.FloatProperty()
    moneyRecieved = db.FloatProperty()


def Project_key(a_key=None):
    return db.Key.from_path('Project', a_key or 'default_key')

class createNewProject(webapp2.RequestHandler):
    def get(self):
        if security.checkSecurityLevel()>9000:
            template = JINJA_ENVIRONMENT.get_template('project.jinja')
            template_values = {
            "name": 'The name of the project',
            "moneyN": 0.0,
            }
            self.response.out.write(template.render(template_values))
    def post(self):
        if security.checkSecurityLevel()>9000:  
            theName=self.request.get('name')
            theMoney=self.request.get('aMoney')
            newProject = Project(key=Project_key(theName))
            newProject.name = theName
            newProject.moneyNeeded =float(theMoney)
            newProject.moneyRecieved = 0.0
            newProject.put()
            template_values = {
            "name": theName,
            "moneyN":theMoney,
           }
            template = JINJA_ENVIRONMENT.get_template('project.jinja')
            self.response.out.write(template.render(template_values))

class displayAllProjects(webapp2.RequestHandler):
    def get(self):
        if security.checkSecurityLevel()>5:
            q = Project.all()
            for p in q.run(limit=20):  
                self.response.out.write(p.name)

           


