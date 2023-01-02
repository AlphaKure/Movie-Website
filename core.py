import flask
import os
import logging
import datetime

from module import user

app=flask.Flask(__name__)
app.logger.setLevel(logging.INFO)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)
userManager=user.User('./database/user.sqlite')


@app.route('/')
def main():
    return flask.render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if flask.request.method=='GET':
        return flask.render_template('login.html')
    isLogin,cookie=userManager.handelUserLogin()
    if not isLogin:
        return flask.redirect('/login')
    else:
        return cookie
    
@app.route('/check')
def check():
    return flask.jsonify({'message':userManager.islogin()})


app.secret_key=os.urandom(16).hex()
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)
