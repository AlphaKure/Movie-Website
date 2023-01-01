from module.base import Base
import flask

class User(Base):

    def __init__(self,userdbPath)->bool:
        super().__init__(userdbPath)
        self.isdbconnect=False if self.database==None else True
    
    def handelUserLogin(self)->bool:
        if self.isdbconnect==False:
            return flask.flash('資料庫問題','error')
        request=flask.request.form.to_dict()
        self.database.cursor()
        if (request['username'],) not in self.database.execute('SELECT username FROM account').fetchall():
            flask.flash('帳號或密碼有誤','error')
            return False
        if (self.hashCal(request['password']),)!= self.database.execute('SELECT password FROM account WHERE username=?',(request['username'],)).fetchone():
            flask.flash('帳號或密碼有誤','error')
            return False
        else:
            flask.flash('登入成功','info')
            return True
        