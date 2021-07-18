# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 22:58:58 2021

@author: AVINASH
"""
from flask import Flask
from flask_restful import Resource,Api, reqparse
from pymongo_client import conn
from users import user
import dateparser as dp
import datetime
import pytz

def utc_time(hour=0):
    utc = pytz.UTC
    cur = datetime.datetime.now()-datetime.timedelta(hours= hour)
    cur = cur.replace(tzinfo=utc)
    
    return str(cur)


class sources(Resource):
    def get(self):
        resp = []
        code = 400
        con =  conn() # to interact with db
        try:
            col, _ = con.get_conn("sources")
            for source in col.find({},{"_id": 0, "rss": 0}):
                resp.append(source)
            code = 200
        finally:
            con.close()
        return {"sources" :resp}, code

class allnews(Resource):
    
    def get(self):
        resp = []
        code = 400
        con =  conn() # to interact with db
        utc= pytz.UTC # for utc time
        low_date = utc_time(3) # default value of low_time =curtime-3h
        up_date = utc_time()
        
        
        # build arguments dict
        url_parser = reqparse.RequestParser()
        url_parser.add_argument('dev_key',required =True)
        url_parser.add_argument('source',default = "", required =False)
        url_parser.add_argument('category',default = "all", required =False)
        url_parser.add_argument('keywords',default = "", required =False)
        url_parser.add_argument('low_date',default = low_date, required = False)
        url_parser.add_argument('up_date',default = up_date, required =False)
        
        # process recieved arguments
        recieved_dict = url_parser.parse_args()
        dev_key = recieved_dict['dev_key']
        
        # check dev_key in db
        try:
            users_col, _ = con.get_conn("users")
            res_devkey = users_col.find_one({"dev_key": dev_key})
            if(not res_devkey):
                return {"msg": "invalid dev_key"}, 200
            if(res_devkey['left_calls'] == 0):
                return {"msg": f"no more api calls left. Will Refresh after {res_devkey['before_time']}"}, 200
            # update calls = calls-1
            res_calls = users_col.update_one({"dev_key": dev_key},{"$set": {"left_calls": res_devkey['left_calls']-1}})
        finally:
            con.close()
            
        source = recieved_dict['source'].split(',')
        category = recieved_dict['category'].split(',')
        keywords = recieved_dict['keywords'].split(',')
        try:
            up_date = dp.parse(recieved_dict['up_date']).replace(tzinfo =utc)
            low_date = dp.parse(recieved_dict['low_date']).replace(tzinfo =utc)
        except:
            return {"error": "Wrong format for low_date and up_date"}, 200
        
        # build query 
        query = {"category": {"$in": category}, \
                 
                 "pub_date": {"$lt": up_date , "$gt":low_date}} 
        
        # processing no inputs from user
        if(recieved_dict['keywords']) :
            query['keywords'] = {"$in":keywords}
        if(recieved_dict['source']):
            query['source'] = {"$in": source}
        
        # collect news in resp
        try:
            col, _ = con.get_conn("news")
            for news in col.find(query,{"_id": 0}):
                news['pub_date']= str(news['pub_date'])
                resp.append(news)
            code = 200
        finally:
            con.close()
        return {"news" :resp}, code



class user_class(Resource):
    def post(self):
        
        
        # build arguments dict
        url_parser = reqparse.RequestParser()
        url_parser.add_argument('email', required = True)
        url_parser.add_argument('pwd', required = True)
        recieved_dict = url_parser.parse_args()
        
        # process arguments
        email = recieved_dict['email']
        pwd = recieved_dict['pwd']
        
        # build user object
        uobj = user(email, pwd)
        resp = uobj.get_user()
        if(resp):
            resp['before_time'] =str(resp['before_time'])
            del resp['_id']
            return resp, 200
        else:
            return {"msg": "Wrong password."}, 200
        
        
        
        
app = Flask(__name__)
api = Api(app)

# to return list of sources
api.add_resource(sources, '/sources')

# to return allnews
api.add_resource(allnews, '/allnews')

# to manage users
api.add_resource(user_class, '/users')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)

