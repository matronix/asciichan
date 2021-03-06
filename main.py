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
import webapp2
import os
import jinja2
import time
import urllib2
import logging
from xml.dom import minidom
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Art(db.Model):
	title = db.StringProperty(required=True)
	art = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

def get_coords(xml):
    TAG_NAME='gml:coordinates'
    #get the document object from the xml string so you can
    #parse it using Document methods such as getElementByTagName()
    doc1 = minidom.parseString(xml)

    #getElementByTagName() will return a NodeList and the item we want is index 0
    e = doc1.getElementsByTagName(TAG_NAME)
    i = e.item(0)

    try:
        if e and i.childNodes[0].nodeValue:
            coords = str(i.childNodes.item(0).data)
            coordsList = coords.split(',')
            return db.GeoPt(coordsList[1],coordsList[0])
        else:
            return None
    except IndexError:
        return None

IP_URL = "http://api.hostip.info/?ip="
def get_coord(ip):
        url = IP_URL + ip
        content = None
        try:
                content = urllib2.urlopen(url).read()
        except URLError:
                return

        if content:
                #parse the returned xml from hostapi.info service
                #and get the lat,lon tuple
                get_coords(content)
CACHE={}     
def top_arts():
          key='top'
          if key in CACHE:
              arts=CACHE[key]
          else:
              logging.error("DBQUERY")      
              arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC LIMIT 10")
	      arts = list(arts)
	      CACHE[key]=arts
	  return arts
	    
class MainHandler(Handler):
    def render_front(self,  title="", art="", error=""):

	    arts = top_arts()
	   
	    self.render("front.html", title=title, art=art, error=error, arts=arts)

    def get(self):
        self.write(repr(self.request.remote_addr))
        self.render_front()

    def post(self):
	    title = self.request.get("title")
	    art = self.request.get("art")

	    if title and art:
		    #self.write('thanks')
		    a = Art(title=title, art=art)
		    #get user's co-ordinates from their ip, if it has coordinates
		    #add then to Art
		    a.put()   
		    time.sleep(0.3)
		    self.redirect("/")
	    else:
		    error = 'Need to enter both title and art'
		    self.render_front(error=error)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
