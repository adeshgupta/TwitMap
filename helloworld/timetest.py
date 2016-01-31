import tweepy,json
import requests.packages.urllib3
from geopy.geocoders import *

requests.packages.urllib3.disable_warnings()
consumer_key = 'cOcBP9hHAUAXGKuQkG0SfMmFD'
consumer_secret = 'I1kjRf6EgyeqStRU0iLZD8DW1bx2MGE0BQNZaDbFJHJI5zg52n'
access_token = '1710334225-gg7M3WtPXLPm0BSde56MaTJyBeO24CohfACUHkD'
access_token_secret = 'HCG0Mp9o9sBkbH4hdLod0vKY7kTyZzeGru2KSzz4OXBwj'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
last_id = -1
max_tweets=100
l=[]
temp=[]
c=0
i=0
geolocator = Nominatim()
while c < max_tweets:
	count = max_tweets - c
	try:
		s = api.search(q="India", count=count, max_id=str(last_id - 1))
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

for x in l:
	print type(x["item"])



