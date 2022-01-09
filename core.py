from os import error
import flask
from check import check

app=flask.Flask(__name__)

isAdmin=False

@app.route('/')
def main():
    return flask.redirect(flask.url_for('Adminlogin'))

@app.route('/login',methods=["POST","GET"])
def Adminlogin():
    global isAdmin
    if flask.request.method == 'POST':
        input_account=flask.request.values.get('account')
        input_password=flask.request.values.get('password')
        isAdmin=check(input_account,input_password)
        if isAdmin==True:
            return flask.redirect(flask.url_for('Dashboard'))
        else:
            return flask.render_template('Adminlogin.html',ERROR='管理員帳號或密碼錯誤')
    return flask.render_template('Adminlogin.html')

@app.route('/Dashboard')
def Dashboard():
    if isAdmin:
        return "Welcome!"
    else:
        return "You don't have Authority!"



if __name__ == '__main__':
     app.run(host='127.0.0.1',port=8000,debug=True)
