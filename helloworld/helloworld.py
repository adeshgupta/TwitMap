import fix_path
import tweepy
import webapp2,json
from datetime import datetime
from geopy.geocoders import *
from google.appengine.api import urlfetch

urlfetch.set_default_fetch_deadline(60)
def min(a,b):
	if(a>b):
		return b
	return a

class MainPage(webapp2.RequestHandler):
    def get(self):
		self.response.headers.add_header("Access-Control-Allow-Origin", "*")
		self.response.headers['Content-Type'] = 'application/json'
		t=str(datetime.now().hour)+":"+str(datetime.now().minute)+":"+str(datetime.now().second)
		obj={'payload':str(t)}
		self.response.out.write(json.dumps(obj))

class MainPage2(webapp2.RequestHandler):
    def get(self):
		self.response.headers.add_header("Access-Control-Allow-Origin", "*")
		self.response.headers['Content-Type'] = 'application/json'
		t='Page2'
		obj={'payload':str(t)}
		self.response.out.write(json.dumps(obj))

class getTrends(webapp2.RequestHandler):
    def get(self):
		consumer_key = 'cOcBP9hHAUAXGKuQkG0SfMmFD'
		consumer_secret = 'I1kjRf6EgyeqStRU0iLZD8DW1bx2MGE0BQNZaDbFJHJI5zg52n'
		access_token = '1710334225-gg7M3WtPXLPm0BSde56MaTJyBeO24CohfACUHkD'
		access_token_secret = 'HCG0Mp9o9sBkbH4hdLod0vKY7kTyZzeGru2KSzz4OXBwj'
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = tweepy.API(auth)
		trends1 = api.trends_place(1) 
		data = trends1[0]
		trends = data['trends']
		names = [trend['name'] for trend in trends]
		self.response.headers.add_header("Access-Control-Allow-Origin", "*")
		self.response.headers['Content-Type'] = 'application/json'
		t=names[:min(len(names),10)]
		obj={'payload':t}
		self.response.out.write(json.dumps(obj))

class test(webapp2.RequestHandler):
    def get(self):
		self.response.headers.add_header("Access-Control-Allow-Origin", "*")
		self.response.headers['Content-Type'] = 'application/json'
		t=self.request.get('trend')
		obj={'payload':str(t)}
		self.response.out.write(json.dumps(obj))

class getLocations(webapp2.RequestHandler):
    def get(self):
		self.response.headers.add_header("Access-Control-Allow-Origin", "*")
		self.response.headers['Content-Type'] = 'application/json'
		consumer_key = 'cOcBP9hHAUAXGKuQkG0SfMmFD'
		consumer_secret = 'I1kjRf6EgyeqStRU0iLZD8DW1bx2MGE0BQNZaDbFJHJI5zg52n'
		access_token = '1710334225-gg7M3WtPXLPm0BSde56MaTJyBeO24CohfACUHkD'
		access_token_secret = 'HCG0Mp9o9sBkbH4hdLod0vKY7kTyZzeGru2KSzz4OXBwj'
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = tweepy.API(auth)
		last_id = -1
		max_tweets=100
		t=str(self.request.get('search'))
		l=[]
		temp=[]
		c=0
		i=0
		geolocator = Nominatim()
		while c < max_tweets:
			count = max_tweets - c
			try:
				s = api.search(q=t, count=count, max_id=str(last_id - 1))
				if not s:
					break
				c+=len(s)
				for x in s:
					y=json.loads(json.dumps(x._json))
					#print y
					if "coordinates" in y and y["coordinates"] is not None:
						a={"type":1,"item":y["coordinates"]["coordinates"]}
						l.append(a)
					elif "location" in y["user"] and y["user"]["location"] not in temp:
						temp.append(y["user"]["location"])
			except tweepy.TweepError as e:
				break
		for x in temp:
			x=x.encode('utf-8')
			location = geolocator.geocode(str(x))
			if location is not None:
				a=[location.latitude,location.longitude]
				d={"type":2,"item":a}
				l.append(d)
		obj={"payload":l}
		self.response.out.write(json.dumps(obj))

app = webapp2.WSGIApplication([
    ('/', MainPage),('/page2',MainPage2),('/gettrends',getTrends),('/test',test),('/getlocations',getLocations)
], debug=True)	
