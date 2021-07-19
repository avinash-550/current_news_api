# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 12:08:03 2021
desc: to manage users of the api
@author: AVINASH
"""
import datetime
import hashlib
from pymongo_client import conn

class user:
    def __init__(self,email, pwd):
        self.email = email
        self.pwd = self.hash_code(pwd)
        
    def gen_new_user(self):
        # To generate new user and add in db
        ind = pytz.timezone('Asia/Kolkata')
       
        # time before no. of calls refresh
        t = datetime.datetime.now(ind) + datetime.timedelta(days =1) 
        
        # to interact with db
        con = conn()
        try:
            col, _ = conn().get_conn("users")
            new_user = {"email": self.email, "pwd": self.pwd, "left_calls": 100,\
                        "before_time":t , "dev_key": self.gen_devkey()}
            res = col.insert_one(new_user)
            del new_user['pwd']
        except:
            return None
        finally:
            con.close()
        if(res):
            return new_user
        else:
            return None 
   
                
    def get_user(self):
        # to get info about user, if not existing create and return info
        if(not self.user_exists()):
            return self.gen_new_user()
        
        con = conn()
        try:
            col, _ = conn().get_conn("users")
            res = col.find_one({"email": self.email, "pwd": self.pwd},\
                               {"email":1, "left_calls":1, "before_time":1, "dev_key":1})
        except:
            return None
        finally:
            con.close()
        if(res):
            return res
        else:
            return None
        
    def user_exists(self):
        # check if user exists in database
        con = conn()
        try:
            col, _ = conn().get_conn("users")
            res = col.find_one({"email": self.email})
        except:
            return False
        finally:
            con.close()
        if(res):
            return True
        else:
            return False
        

    def gen_devkey(self):
        ind = pytz.timezone('Asia/Kolkata')
        # generates and returns developer unique key
        return datetime.datetime.now(ind).strftime('%Y%m%d%H%M%S%f')
    
    def hash_code(self,string):
        # generates and returns hash of the given string
        hash_obj = hashlib.sha256(string.encode('utf-8'))
        return hash_obj.hexdigest()
        
        
