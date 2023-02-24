import flask
import os
import logging
import datetime

from module import user

app=flask.Flask(__name__)
app.logger.setLevel(logging.INFO)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)
userManager=user.UserManager('./database/user.sqlite')

@app.template_global()
def isLogin():
    return userManager.loginAuth()

@app.route('/')
def main():
    return flask.render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if flask.request.method=='GET':
        return flask.render_template('login.html')
    return userManager.userLogin()
    
@app.route('/logout')
def logout():
    return userManager.userLogout()

@app.route('/register',methods=['GET','POST'])
def register():
    if flask.request.method=='GET':
        return flask.render_template('/register.html')
    return userManager.userRegister()

'''Test for session 
@app.route('/uuid')
def uuid():
    return flask.jsonify({'message':flask.session.get(flask.request.cookies.get('uuid'))})
'''
app.secret_key=os.urandom(16).hex()
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)
