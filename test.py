# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 18:50:04 2021

@author: AVINASH
"""
import pymongo
from pymongo_client import conn
import dateparser
client = pymongo.MongoClient("mongodb+srv://avinashlocal:5sr3Yhp8fzt9PL27@cluster0.kbfok.mongodb.net/news_current?retryWrites=true&w=majority")
db = client.news_current

client.close()
col = db["sources"]

col, _ = conn().get_conn("news")
x['_id'] = '2423423'
y = col.insert_one(x)
col.close()
query = {"source":{"$in": ['dna', 'deccanchronicle']}, "category": {"$in": ['sports', 'all']}, "keywords": {"$in":[ 'state', 'places']}}
query = {"source":{"$in": ['dna', 'deccanchronicle']},"pub_date": {"$lt": dateparser.parse('2021-07-18T02:30:47.000+00:00') , "$gt":dateparser.parse('2021-07-16T02:30:47.000+00:00')}} 

filt = {"_id": 0}
c=0
for i in col.find(query, filt):
    print(i['title'])
    print(i['pub_date'])
    c+=1
    print(c)
    
with conn().get_conn("sources") as col:
    for i in col[0].find({}):
        print(i['name'])
from newspaper import Article


url = "https://www.thehindu.com/news/national/ncp-chief-sharad-pawar-meets-pm-narendra-modi/article35378794.ece"

article= Article(url)
article.download()
article.parse()
article.nlp()
print(article.summary)
print(article.publish_date)


import feedparser
import dateparser
feed = "https://www.dnaindia.com/feeds/india.xml"

f = feedparser.parse(feed)
for i in f['items']:
    print(dateparser.parse(i['published']))
    print(i['title'])
    print(i['link'])
    print(i['summary'])
    
    
import datetime
import pytz

utc = pytz.UTC
cur =datetime.datetime.now(pytz.utc)
newd = cur - datetime.timedelta(minutes = 58)

from curate_news import curater

c =curater("https://www.dnaindia.com/feeds/india.xml")
c.curate_rss()
h = c.get_resp()


from users import user

u = user("avi@gmail.com", "secret")
x = u.get_user()