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

def id_generator(size=10, chars=string.digits):
    return ''.join(random.choice(chars) for x in range(size))


class LevelGraphic(db.Model):
    createDate = db.DateTimeProperty(auto_now_add = True)
    data = db.TextProperty()
    background = db.BlobProperty()
    ball = db.BlobProperty()

def LevelGraphic_key(a_key=None):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return db.Key.from_path('LevelGraphic', a_key or 'default_key')

class SaveJsonData(webapp2.RequestHandler):
    def post(self):
        getInfo = self.request.get('Data')
        
        id = id_generator()
        checkValue = LevelGraphic.get(LevelGraphic_key(id))
        while checkValue:
            id = id_generator()
            checkValue = LevelGraphic.get(LevelGraphic_key(id))
        
        checkValue = LevelGraphic(key=LevelGraphic_key(id))
        
        checkValue.data = getInfo
        checkValue.background = self.request.get('Background')
        checkValue.ball = self.request.get('Ball')
        
        checkValue.put();
        self.response.out.write(id)

class loadBackGround(webapp2.RequestHandler):
    def get(self):
        id = self.request.get('id')
        checkValue = LevelGraphic.get(LevelGraphic_key(id))
        if checkValue:
            self.response.headers['Content-Type'] = 'image/jpg'
            self.response.out.write(checkValue.background)
        else:
            self.error(404)


class loadBall(webapp2.RequestHandler):
    def get(self):
        id = self.request.get('id')
        checkValue = LevelGraphic.get(LevelGraphic_key(id))
        if checkValue:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(checkValue.ball)
        else:
            self.error(404)

class loadJson(webapp2.RequestHandler):
    def get(self):
        id = self.request.get('id')
        checkValue = LevelGraphic.get(LevelGraphic_key(id))
        if checkValue:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(checkValue.data)
        else:
            self.error(404)



