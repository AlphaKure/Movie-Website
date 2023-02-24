import flask
import datetime
import sqlite3

from module.base import Base

class UserManager(Base):

    def __init__(self,DBPath)->None:
        super().__init__(DBPath)

    def userLogin(self)->flask.Response:
        self.databaseState()
        resp=flask.make_response(flask.redirect('/login'))
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
        self.databaseState()
        self.database.cursor()
        resp=flask.make_response(flask.redirect('/register'))
        request=flask.request.form.to_dict()
        if request['password']!=request['confirmPassword']:
            flask.flash('密碼不一致',category='error')
            return resp
        if self.database.execute('SELECT * FROM account WHERE username=?',(request['account'],)).fetchone()!=None:
            flask.flash('帳號已存在',category='error')
            return resp
        # 都沒問題 以後可以再增加密碼複雜驗證etc
        self.database.execute('INSERT INTO account(username,password,email,isAdmin) VALUES(?,?,?,0)',(request['account'],self.hashCal(request['password']),request['email']))
        self.database.commit()
        resp=flask.make_response(flask.redirect('/login'))
        flask.flash('註冊成功!請重新登入',category='info')
        return resp
            

class User:

    def __init__(self,username,DB:sqlite3.Connection) -> None:
        getData=DB.execute('SELECT * FROM account WHERE username=?',(username,)).fetchone()
        if getData!=None:
            self.username=username
            self.password=getData[1]
            self.email=getData[2]
            self.nickname=getData[3]
            self.isAdmin=True if getData[4]==1 else False
        
    