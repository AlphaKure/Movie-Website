import flask
import datetime
import sqlite3

from module.base import Base

class UserManager(Base):

    def __init__(self,DBPath)->None:
        super().__init__(DBPath)
        self.isDBconnect=False if self.database==None else True

    def userLogin(self)->flask.Response:
        resp=flask.make_response(flask.redirect('/login'))
        if self.isDBconnect==False:
            flask.flash('資料庫問題，請聯繫管理員','error')
            return resp
        request=flask.request.form.to_dict()
        self.database.cursor()
        if (request['username'],) not in self.database.execute('SELECT username FROM account').fetchall():
            flask.flash('帳號或密碼有誤','error')
            return resp
        if (self.hashCal(request['password']),)!= self.database.execute('SELECT password FROM account WHERE username=?',(request['username'],)).fetchone():
            flask.flash('帳號或密碼有誤','error')
            return resp
        else:
            # 成功登入 
            expireTime=datetime.datetime.now()+datetime.timedelta(days=7)
            uuid=Base.hashCal(request['username'])
            flask.session[uuid]=User(request['username'],self.database).__dict__
            flask.session.permanent=True
            resp=flask.make_response(flask.redirect('/'))
            resp.set_cookie('uuid',uuid,expires=expireTime)
            return resp
    
    def loginAuth(self)->bool:
        return True if flask.session.get(flask.request.cookies.get('uuid')) else False

    def userLogout(self)->flask.Response:
        uuid=flask.request.cookies.get('uuid')
        flask.session[uuid]=False
        resp=flask.make_response(flask.redirect('/'))
        resp.delete_cookie('uuid')
        return resp
    
    def userRegister(self):
        request=flask.request.form.to_dict()
        

class User:

    def __init__(self,username,DB:sqlite3.Connection) -> None:
        getData=DB.execute('SELECT * FROM account WHERE username=?',(username,)).fetchone()
        if getData!=None:
            self.username=username
            self.password=getData[1]
            self.email=getData[2]
            self.nickname=getData[3]
            self.isAdmin=True if getData[4]==1 else False
        
    