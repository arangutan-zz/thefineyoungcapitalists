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

import json

import jinja2
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.api import images
from google.appengine.ext import blobstore

import string
import random
import counter
import hashlib




def id_generator(size=40, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def id_short(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True
                                       
                                       )

class Cause(ndb.Model):
    createDate = ndb.DateTimeProperty(auto_now_add = True)
    location = ndb.FloatProperty(indexed=True, default=10)
    user = ndb.UserProperty(indexed=True)
    name = ndb.StringProperty(indexed=True)
    BTCAdress = ndb.StringProperty(indexed=True)
    description = ndb.TextProperty()
    avatar = ndb.BlobProperty()
    youtube = ndb.StringProperty()
    hasYoutube = ndb.BooleanProperty()
    isVisible = ndb.BooleanProperty(indexed=True)
    id = ndb.StringProperty(indexed=True)

def Cause_key(a_key=None):
    return ndb.Key('Cause', a_key)

class BitCoin(ndb.Model):
    transactionID = ndb.StringProperty()
    amountBTC = ndb.FloatProperty()
    amountNative = ndb.FloatProperty()
    amountType = ndb.StringProperty()
    createDate = ndb.DateTimeProperty(auto_now_add = True)
    project = ndb.IntegerProperty(indexed=True)
    email = ndb.StringProperty()
    claimed = ndb.BooleanProperty()
    user = ndb.UserProperty(indexed=True)

def BitCoin_key(a_key=None):
    return ndb.Key('BitCoin', a_key)

class BitCoinReturn(webapp2.RequestHandler):
    #def post(self):
    def get(self):    
        #inputData = self.request.body
        inputData = '''
		{
  "order": {
    "id": "5RTQNACF",
    "created_at": "2012-12-09T21:23:41-08:00",
    "status": "completed",
    "total_btc": {
      "cents": 100000000,
      "currency_iso": "BTC"
    },
    "total_native": {
      "cents": 1253,
      "currency_iso": "USD"
    },
    "custom": "order1234",
    "receive_address": "1NhwPYPgoPwr5hynRAsto5ZgEcw1LzM3My",
    "button": {
      "type": "buy_now",
      "name": "Alpaca Socks",
      "description": "The ultimate in lightweight footwear",
      "id": "5d37a3b61914d6d0ad15b5135d80c19f"
    },
    "transaction": {
      "id": "514f18b7a5ea3d630a00000f",
      "hash": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
      "confirmations": 0
    },
    "customer": {
      "email": "mrappard@gmail.com",
      "shipping_address": [
        "John Smith",
        "123 Main St.",
        "Springfield, OR 97477",
        "United States"
      ]
    }
  }
}
'''
        id = id_generator()
        checkValue = BitCoin.query(ancestor=BitCoin_key(id))
        theData = json.loads(inputData)
        #while checkValue:
        #    id = id_generator()
        #    checkValue = BitCoin.query(ancestor=BitCoin_key(id))
        checkValue = BitCoin(key=BitCoin_key(id))
        checkValue.transactionID = theData['order']['id']
        checkValue.amountBTC = theData['order']['total_btc']['cents']
        checkValue.amountNative = theData['order']['total_native']['cents']
        checkValue.amountType =  theData['order']['total_native']['currency_iso']
        checkValue.project =  1
        checkValue.claimed = False
        checkValue.email = theData['order']['customer']['email']
        checkValue.put();
        




        
        sender_address = 'admin@thefineyoungcapitalists.com'
        user_address = theData['order']['customer']['email']
        subject = "Thank you for your support"
        body = '''Your payement of %s BTC has been recieved by The Fine Young Capitalists.

Please follow this web adress <a href="http://www.thefineyoungcapitalists.com/LinkToAccount?id=%s">http://www.thefineyoungcapitalists.com/LinkToAccount?id=%s</a> to link your purchase to your Google Account so you can vote and choose a target for your profits.

''' % (theData['order']['total_btc']['cents'],id,id)

        mail.send_mail(sender_address, user_address, subject, body)
        self.response.out.write(body)

#Attach the Bitcoin to an account
class BitCoinID(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            id = self.request.get('id')
            if (id):
                checkValue = BitCoin.get_by_id(id)
                if (checkValue):
                    if (checkValue.claimed is False):
                        checkValue.claimed = True;
                        checkValue.user = user
                        checkValue.put()
                        self.response.out.write('''<meta http-equiv="refresh" content="0; url=/Profile" />''');
                    else:
                        self.response.out.write("This ID has already been claimed")
                else:
                    self.response.out.write("This ID is not valid")
            else:
                self.response.out.write("This ID is not valid")
        else:
            self.response.out.write("Your not logged in")

#Warn the User they are about to attach a Bitcoin
class BitCoinID_HoldPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            id = self.request.get('id')
            if (id):
                checkValue = BitCoin.get_by_id(id)
                if (checkValue):
                    if (checkValue.claimed is False):
                        template = JINJA_ENVIRONMENT.get_template('BitCoin_HoldPage.jinja')
                        template_values = {
                        "Name": user.nickname(),
                        "BTC": checkValue.amountBTC,
                        "Price":checkValue.amountNative,
                        "TypeOfMoney":checkValue.amountType,
                        "ID":id
                        }
                        self.response.out.write(template.render(template_values))
                    else:
                        self.response.out.write("This ID has already been claimed")
                else:
                    self.response.out.write("This ID is not valid")
            else:
                self.response.out.write("This ID is not valid")
        else:
            url = '/LinkToAccount'
            self.response.out.write('''<meta http-equiv="refresh" content="0; url=%s" />''' % users.create_login_url(url));

#Display All The BitCoin Inputs
class Display_BitCoinID(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            qry = BitCoin.query(BitCoin.user==user).fetch()
            for ent in qry:
                self.response.out.write('%s,%s,%s<br>' %(ent.amountBTC, ent.transactionID, ent.createDate ))

#Display All The BitCoin Inputs
class Profile(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            qry = BitCoin.query(BitCoin.user==user).fetch()
            amountOfCoin = 0
            for ent in qry:
                amountOfCoin = amountOfCoin + ent.amountBTC
            self.response.out.write('%s<br>' %(amountOfCoin))
        else:
            url = '/Profile'
            self.response.out.write('''<meta http-equiv="refresh" content="0; url=%s" />''' % users.create_login_url(url));


class CreateCause(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            cause = Cause.get_by_id(user.user_id())
            if cause ==  None:
                
                cause = Cause(key=Cause_key(user.user_id()))
                cause.user = user
                cause.name = "Please Create A Name"
                cause.description = "Please Describe Your Group"
                cause.BTCAdress = "Please Include a Bitcoin address to send your profits"
                cause.youtube = "Please Include a Youtube Address."
                cause.hasYoutube = False
                cause.isVisible  = False
                cause.id = id_short()
                cause.put()
            template = JINJA_ENVIRONMENT.get_template('Cause.jinja')
            template_values = {
                "Name": cause.name,
                "Description": cause.description,
                "BTCAdress":cause.BTCAdress,
                "Youtube":cause.youtube,
                "HasYoutube":cause.hasYoutube,
                "IsVisible":cause.isVisible
                    }
            self.response.out.write(template.render(template_values))
        else:
            url = '/SubmitCause'
            self.response.out.write('''<meta http-equiv="refresh" content="0; url=%s" />''' % users.create_login_url(url));         
    def post(self):
        user = users.get_current_user()
        if user:
            cause = Cause.get_by_id(user.user_id())
            if cause ==  None:
                cause = Cause(key=Cause_key(user.user_id()))
                cause.user = user
                cause.name = "Please Create A Name"
                cause.description = "Please Describe Your Group"
                cause.BTCAdress = "Please Include a Bitcoin address to send your profits"
                cause.youtube = "Please Include a Youtube Address."
                cause.hasYoutube = False
                cause.isVisible  = False
            cause.name = self.request.get('Name')
            cause.description = self.request.get('Description')
            cause.BTCAdress = self.request.get('BTCAdress')
            cause.youtube = self.request.get('Youtube')
            cause.put()
            template = JINJA_ENVIRONMENT.get_template('Cause.jinja')
            template_values = {
                "Name": cause.name,
                "Description": cause.description,
                "BTCAdress":cause.BTCAdress,
                "Youtube":cause.youtube,
                "HasYoutube":cause.hasYoutube,
                "IsVisible":cause.isVisible
                    }
            self.response.out.write(template.render(template_values))
        else:
            url = '/SubmitCause'
            self.response.out.write('''<meta http-equiv="refresh" content="0; url=%s" />''' % users.create_login_url(url)); 


class SubmitCauseImage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            template = JINJA_ENVIRONMENT.get_template('Cause_ImagePost.jinja')
            self.response.out.write(template.render())
    def post(self):
        user = users.get_current_user()
        if user:
            cause = Cause.get_by_id(user.user_id())
            avatar = images.resize(self.request.get('img'), 32, 32)
            #upload_files = self.get_uploads('logo_img')
            cause.avatar = avatar
            cause.put()
        self.redirect('/SubmitCause')


class CauseImage(webapp2.RequestHandler):
    def get(self):
        id = self.request.get('id')
        qry = Cause.query(Cause.id==id).fetch(limit=1)
        for ent in qry:
            if ent.avatar:
                self.response.headers['Content-Type'] = 'image/png'
                self.response.out.write(ent.avatar)
            else:
                self.error(404)

class ViewAllCauses(webapp2.RequestHandler):
    def get(self):
        step = self.request.get('step')
        qry = Cause.query().order(Cause.location).fetch(limit=12)
        array = []
        object = []
        for ent in qry:
            object.append(ent.id)
            if len(object)==3:
                array.append(object)
                object = []
        if len(array)<4:
            if len(object) is not 0:
                while len(object)<3:
                    object.append("Test")
        array.append(object)
        template = JINJA_ENVIRONMENT.get_template('View_All_Causes.jinja')
        template_values = {
                "Causes": array
                    }
        self.response.out.write(template.render(template_values))


class EditCauses(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            id = self.request.get('id')
            qry = Cause.query(Cause.id==id).fetch(limit=1)
            for cause in qry:
                template = JINJA_ENVIRONMENT.get_template('CauseEdit.jinja')
                template_values = {
                "Name": cause.name,
                "Description": cause.description,
                "BTCAdress":cause.BTCAdress,
                "Youtube":cause.youtube,
                "HasYoutube":cause.hasYoutube,
                "IsVisible":cause.isVisible
                    }
                self.response.out.write(template.render(template_values))
        else:
            url = '/EditCauses'
            self.response.out.write('''<meta http-equiv="refresh" content="0; url=%s" />''' % users.create_login_url(url));         
    def post(self):
        user = users.get_current_user()
        if user:
            id = self.request.get('id')
            qry = Cause.query(Cause.id==id).fetch(limit=1)
            for cause in qry:
                cause.name = self.request.get('Name')
                cause.description = self.request.get('Description')
                cause.BTCAdress = self.request.get('BTCAdress')
                cause.youtube = self.request.get('Youtube')
                cause.put()
                template = JINJA_ENVIRONMENT.get_template('CauseEdit.jinja')
                template_values = {
                    "Name": cause.name,
                    "Description": cause.description,
                    "BTCAdress":cause.BTCAdress,
                    "Youtube":cause.youtube,
                    "HasYoutube":cause.hasYoutube,
                    "IsVisible":cause.isVisible
                    }
                self.response.out.write(template.render(template_values))
        else:
            url = '/EditCauses'
            self.response.out.write('''<meta http-equiv="refresh" content="0; url=%s" />''' % users.create_login_url(url)); 

class Submit_Cause_Image_ID(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            id = self.request.get('id')
            template_values = {
            "ID":id
            }
            template = JINJA_ENVIRONMENT.get_template('Cause_ImagePost_ID.jinja')
            self.response.out.write(template.render(template_values))
    def post(self):
        user = users.get_current_user()
        if user:
            id = self.request.get('id')
            qry = Cause.query(Cause.id==id).fetch(limit=1)
            for cause in qry:
                avatar = images.resize(self.request.get('img'), 32, 32)
                #upload_files = self.get_uploads('logo_img')
                cause.avatar = avatar
                cause.put()
        self.redirect('/EditCauses')

class CreateBaseCauses(webapp2.RequestHandler):
    def get(self):
        for x in range(0, 12):
            cause = Cause(key=Cause_key(x))
            cause.name = "Please Create A Name"
            cause.description = "Please Describe Your Group"
            cause.BTCAdress = "Please Include a Bitcoin address to send your profits"
            cause.youtube = "Please Include a Youtube Address."
            cause.hasYoutube = False
            cause.isVisible  = False
            cause.id = id_short()
            cause.put()
        self.response.out.write("Create Base Causes")