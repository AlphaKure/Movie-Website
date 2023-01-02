import flask
import os
import logging
import datetime

from module import user

app=flask.Flask(__name__)
app.logger.setLevel(logging.INFO)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)
userManager=user.User('./database/user.sqlite')

@app.template_global()
def isLogin():
    return userManager.isLogin()

@app.route('/')
def main():
    return flask.render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if flask.request.method=='GET':
        return flask.render_template('login.html')
    isLogin,cookie=userManager.userLogin()
    if not isLogin:
        return flask.redirect('/login')
    else:
        return cookie
    
@app.route('/logout')
def logout():
    return userManager.userLogout()

'''Test for session 
@app.route('/uuid')
def uuid():
    return flask.jsonify({'message':userManager.uuidDict})
'''
app.secret_key=os.urandom(16).hex()
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)
