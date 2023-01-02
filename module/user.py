import flask
import datetime

from module.base import Base

class User(Base):

    def __init__(self,userdbPath):
        super().__init__(userdbPath)
        self.isdbconnect=False if self.database==None else True
        self.uuidDict=dict()

    def userLogin(self):
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
            # 成功登入 
            expiretime=datetime.datetime.now()+datetime.timedelta(days=7)
            uuid=Base.hashCal(request['username'])
            flask.session[uuid]=True
            flask.session.permanent=True
            self.uuidDict[request['username']]=uuid
            cookie=flask.make_response(flask.redirect('/'))
            cookie.set_cookie('uuid',uuid,expires=expiretime)
            return True,cookie
    
    def isLogin(self):
        return True if flask.session.get(flask.request.cookies.get('uuid')) else False

    def userLogout(self):
        flask.session[flask.request.cookies.get('uuid')]=False
        self.uuidDict.pop(flask.request.cookies.get('uuid'))
        resp=flask.make_response(flask.redirect('/'))
        resp.delete_cookie('uuid')
        return resp