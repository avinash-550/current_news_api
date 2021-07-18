# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 21:44:36 2021
description : loads new news article within delta time. Runs every delta time on server.
also deletes obselete articles from db(of before 7 days)
also refreshes user calls_left tally to 100
@author: AVINASH
"""
from pymongo_client import conn
from curate_news import curater
import sys
import datetime
import pytz

if __name__ == "__main__":
    logmsg = f"{datetime.datetime.now()}" # to keep a log\
    # to interact with mongodb
    con = conn()
    
    # refresh call_left for users to 100
    try:
        user_col, _ = con.get_conn("users")
        t = datetime.datetime.now() + datetime.timedelta(days =1)
        query = {"before_time" : {"$lt":datetime.datetime.now()}}
        updated = {"$set": {"before_time": t, "left_calls" : 100}}
        temp = user_col.update_many(query, updated)
    except:
        logmsg += " couldn't refresh calls for users from db!"

    # cal date of 7 days prior
    utc = pytz.UTC
    least_time = datetime.datetime.now(pytz.utc) - datetime.timedelta(days = 7)
    
    # delete articles from 7 days earliar
    try:
        news_col, _ = con.get_conn("news")
        temp = news_col.delete_many({"pub_date":{"$lt": least_time}})
    except:
        logmsg += " couldn't delete from db!"
    
    # create list of sources in db
    source_list = []
    sources_col, sts = con.get_conn("sources")
    if(not sts):
        sys.exit(0)
        
    for source in sources_col.find({}):
        source_list.append({"name" :source['name'],"category" :source['category'], "rss": source['rss']})
        
    
    # create help_array with existing news in db
    help_array = []
    news_col, sts = con.get_conn("news")
    if(not sts):
        sys.exit(0)
    
    for title in news_col.find({},{'title': 1}):
        help_array.append(title['title'])
           
    # Get fresh articles into new_news
    new_news =[]
    
    for source in source_list:
        curate_obj = curater(source['rss'] , source['category'], source['name'] , help_array)
        curate_obj.curate_rss()
        # extend to add news from this rss
        new_news.extend(curate_obj.get_resp())
    
    # update db
    try:
        col_affected = news_col.insert_many(new_news)
        logmsg += " updated db succesfully."
    except:
        logmsg += " couldn't update db."
        
    try:
        load_col, sts = con.get_conn("load_news")
        load_col.insert_one({"msg": logmsg})
    except: 
        pass
    
    con.close() #close db connection
    
    
        
        
    