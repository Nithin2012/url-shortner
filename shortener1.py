import webapp2
import random
import cgi

from google.appengine.api import users
from google.appengine.ext import db

class Data(db.Model):
	longurl=db.StringProperty(multiline=True)
	shorturl=db.StringProperty()

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("""
          	<html>
            	<body>
		<br/><br/><br/><br/><br/><br/><br/><br/>
		<center>
		Please Enter the Long url
              	<form >
                <div><textarea name="longurl" rows="3" cols="100"></textarea></div>
		<div><textarea name="getcount" rows="3" cols="100"></textarea></div>
                <div><input type="submit" value="Convert"></div>
              	</form></center>""")
		longurl=self.request.get('longurl')
		l = len(longurl)
		lis = []
		shorturl = []
		for i in range(l) :
			if i % 8 == 0:
				lis.append(longurl[i])
			shorturl = ''.join(lis)
		if longurl != "":
			obj=Data(db.Key.from_path('Table',longurl))
			obj.longurl=longurl
			obj.shorturl=shorturl
			getdata=db.GqlQuery("SELECT * FROM Data WHERE ANCESTOR IS :a",a=db.Key.from_path('Table',longurl))
			cnt =0
			for i in getdata:
				cnt=cnt+1
			if cnt==0:
				obj.put()
			short=self.request.path[1:]
			getdata1=db.GqlQuery("SELECT * FROM Data WHERE ANCESTOR IS :a",a=db.Key.from_path('Table',longurl))
			
			for i in getdata1:
				self.response.out.write("<center><br/><br/>short Url")
				self.response.out.write("<br/><br/>""nithinshorturl.appspot.com/")
				self.response.out.write(i.shorturl)
				self.response.out.write("""<br></font></center>""")
			self.response.out.write("""</body></html>""")
		if self.request.path[1:]!="":
			fetch=Data.all()
			final = fetch.filter("shorturl =",self.request.path[1:]).get()
			self.redirect(str(final.longurl))			

app=webapp2.WSGIApplication([('/.*',MainPage)],debug=True)		
