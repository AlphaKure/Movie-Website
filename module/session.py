import os
import flask

class Session:

    def __init__(self) -> None:
        self.tokenlist=list()

    def addToken(self,username)->str:
        newToken=os.urandom(24).hex()
        isExist=False
        for token in self.tokenlist:
            if token['username']==username:
                token['token']=newToken
                isExist=True
        if not isExist:
            self.tokenlist.append({'username':username,'token':newToken})
        return newToken
        
    def islogin(self):
        user=flask.request.cookies.get('username')
        key=flask.request.cookies.get('token')
        for token in self.tokenlist:
            if user==token['username'] and key==token['token']:
                return True
        return False