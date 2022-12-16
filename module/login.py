import flask
import logging
import sqlite3

class login :

    def __init__(self)->None:
        
        try:
            self.sqlite3.connect('./database/user.sqlite')
        except:
            pass

    def userRegister():
        pass