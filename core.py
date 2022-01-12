import flask
from check import check
from register import register

app=flask.Flask(__name__)

islogin=False
isAdmin=False
nowuser=""

@app.route('/')
def main():
    return flask.redirect(flask.url_for('Home'))

@app.route('/Adminlogin',methods=["POST","GET"])
def Adminlogin():
    global isAdmin
    if isAdmin==True:
        return flask.redirect(flask.url_for('Dashboard'))
    else:
        if flask.request.method == 'POST':
            input_account=flask.request.values.get('account')
            input_password=flask.request.values.get('password')
            isAdmin=check(input_account,input_password,"Admin")
            if isAdmin==True:
                return flask.redirect(flask.url_for('Dashboard'))
            else:
                return flask.render_template('Adminlogin.html',ERROR='管理員帳號或密碼錯誤')
        return flask.render_template('Adminlogin.html')

@app.route('/Dashboard',methods=["POST","GET"])
def Dashboard():
    global isAdmin
    if flask.request.method=='POST':
            isAdmin=False
            return flask.redirect(flask.url_for('Adminlogin'))
    if isAdmin:
        return flask.render_template('Dashboard.html')
    else:
        return "You don't have Authority!"

@app.route('/login',methods=["POST","GET"])
def login():
    global islogin
    global nowuser
    if flask.request.method=='POST':
        input_account=flask.request.values.get('Username')
        input_password=flask.request.values.get('Password')
        islogin=check(input_account,input_password,"user")
        if islogin==True:
            nowuser=input_account
            return flask.redirect(flask.url_for('Home'))
        else:
            flask.flash('登入失敗 請確認帳號和密碼')
    return flask.render_template('login.html',islogin=islogin)

@app.route('/logout')
def logout():
    global islogin
    global nowuser
    nowuser=""
    islogin=False
    return flask.redirect(flask.url_for('Home'))

@app.route('/home')
def Home():
    return flask.render_template('come_soon.html',islogin=islogin)

if __name__ == '__main__':
    app.secret_key="Movie-website"
    app.run(host='127.0.0.1',port=8000,debug=True)
