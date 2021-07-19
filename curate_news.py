# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 20:09:08 2021

@author: AVINASH
"""
import dateparser as dp
import feedparser
from newspaper import Article
import datetime
import pytz

class curater:
    # curates last hour articles coming on rss and returns as list
    
    def __init__(self, rss,category = "all",source = "unknown", arr=[], time_gap = 1):
        self.rss = rss
        self.resp = []
        self.help_array = arr # db array of articles to avoid adding same articles
        self.past_time_limit = self.__get_past__(time_gap)
        self.category =category # type of news
        self.source  = source # name of news agency
        
    def __get_past__(self, time_gap):
        # cal current utc time
        ind = pytz.timezone('Asia/Kolkata')
        curtime = datetime.datetime.now(ind)
        
        # cal 1 hour before time in UTC, 2 minutes less for large processing
        past_time = curtime - datetime.timedelta(hours = time_gap)
        return past_time
        
    def curate_url(self, url, feedobj):
        """Curates a particular url with help of Article and feedparser object"""
        build_res = {}
        utc = pytz.UTC # for utc time
        
        # info using feedparser
        try:
            build_res['pub_date'] = dp.parse(feedobj['published']).replace(tzinfo =utc)
        except:
            return None
        
        build_res['title'] = feedobj['title']
        
        build_res['url'] = url
        
        # check if article already exists in db or came before  past time limit
        if  build_res['title'] in self.help_array or build_res['pub_date']<=self.past_time_limit:
            return None
        
        # info using Article, newspaper3k
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            summary = article.summary
            image = article.top_image
            text = article.text
            keyword = article.keywords
        except:
            summary=image=text = "not available"
            keyword= []
        # add info obtained if available 
        build_res['description'] = summary.split('.')[0] # first sentence of summary
        build_res['summary'] = summary
        build_res['image'] = image
        build_res['content'] = text
        build_res['source'] = self.source
        build_res['category'] =self.category
        build_res['keywords']= keyword
        
        # update self_help_array
        self.help_array.append(build_res['title'])
        
        return build_res
    
    def curate_rss(self):
        # parse rss link
        try:
            self.parser = feedparser.parse(self.rss)
        except:
            return 
        # curate for all news items
        for feedobj in self.parser['items']:
            curated_url = self.curate_url(feedobj['link'], feedobj)
            # if not none add to resp
            if(curated_url!=None):
                self.resp.append(curated_url)
            
        
    def get_resp(self):
        return self.resp
            
        
         
        
        
