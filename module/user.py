import flask
import datetime
import os

from module.base import Base

class User(Base):

    def __init__(self,userdbPath):
        super().__init__(userdbPath)
        self.isdbconnect=False if self.database==None else True

    def handelUserLogin(self):
        if self.isdbconnect==False:
            flask.flash('資料庫問題，請聯繫管理員','error')
            return False,None
        request=flask.request.form.to_dict()
        self.database.cursor()
        if (request['username'],) not in self.database.execute('SELECT username FROM account').fetchall():
            flask.flash('帳號或密碼有誤','error')
            return False,None
        if (self.hashCal(request['password']),)!= self.database.execute('SELECT password FROM account WHERE username=?',(request['username'],)).fetchone():
            flask.flash('帳號或密碼有誤','error')
            return False,None
        else:
            expiretime=datetime.datetime.now()+datetime.timedelta(days=7)
            token=os.urandom(32).hex()
            flask.session[request['username']]=token
            flask.session.permanent=True
            cookie=flask.make_response(flask.redirect('/'))
            cookie.set_cookie('token',token,expires=expiretime)
            cookie.set_cookie('username',request['username'],expires=expiretime)
            return True,cookie
    
    def islogin(self):
        return True if flask.session.get(flask.request.cookies.get('username'))==flask.request.cookies.get('token') else False


        