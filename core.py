import flask
from check import check

app=flask.Flask(__name__)

islogin=False
isAdmin=False

@app.route('/')
def main():
    return flask.redirect(flask.url_for('login'))

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
    if flask.request.method=='POST':
        input_account=flask.request.values.get('Username')
        input_password=flask.request.values.get('Password')
        islogin=check(input_account,input_password,"user")
        if islogin==True:
            return "Welcome!"
        else:
            return "Error!"
    return flask.render_template('login.html')


if __name__ == '__main__':
     app.run(host='127.0.0.1',port=8000,debug=True)
