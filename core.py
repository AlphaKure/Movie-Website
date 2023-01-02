import flask
import os

from module import user,session

app=flask.Flask(__name__)

sessionManager=session.Session()
userManager=user.User('./database/user.sqlite',sessionManager=sessionManager)


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
    return flask.jsonify(sessionManager.islogin())

@app.route('/session')
def sessions():
    return flask.jsonify(sessionManager.tokenlist)

app.secret_key=os.urandom(16).hex()
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)
