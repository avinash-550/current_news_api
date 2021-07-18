# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 17:13:20 2021

@author: AVINASH
"""

import pymongo

# mongo uri
MONGO_URI = "mongodb+srv://avinashlocal:5sr3Yhp8fzt9PL27@cluster0.kbfok.mongodb.net/news_current?retryWrites=true&w=majority"

class conn:
    def __init__(self):
        # to refer to a particular collection in db
        self.status = 1
        self.maindb_client = pymongo.MongoClient(MONGO_URI)
        self.db_client = self.maindb_client.news_current
        
    def get_conn(self, collection):
        """ Gets mongodb connection object and returns it"""
        try:
            client = self.db_client[collection]
        except:
            # set status as 0 to indicate client couldn't be made
            self.status = 0
            return None, False
        
        return client, True
    def close(self):
        self.maindb_client.close()
        