import flask
from check import check
from register import register_acc

app=flask.Flask(__name__)

isAdmin=False
nowuser=""

@app.template_global()
def getcookie():
    return True if flask.request.cookies.get('logged_in') == "Y" else False

@app.route('/')
def main():
    return flask.redirect(flask.url_for('Home'))

@app.route('/home')
def Home():
    return flask.render_template('come_soon.html')

@app.route('/login',methods=["POST","GET"])
def login():
    global nowuser
    if flask.request.method=='POST':
        input_account=flask.request.values.get('Username')
        input_password=flask.request.values.get('Password')
        if check(input_account,input_password,"user"):
            nowuser=input_account
            resp = flask.make_response(flask.redirect('/home'))
            resp.set_cookie('logged_in',"Y",expires=None)
            return resp
        else:
            flask.flash('登入失敗 請確認帳號和密碼')
    return flask.render_template('login.html')

@app.route('/logout')
def logout():
    global nowuser
    nowuser=""
    resp = flask.make_response(flask.redirect('/home'))
    resp.set_cookie('logged_in',"N",expires=0)
    return resp

@app.route('/register',methods=["POST","GET"])
def register():
    if flask.request.method=='POST':
        input_account=flask.request.values.get('account')
        input_password=flask.request.values.get('password')
        check_password=flask.request.values.get('c_password')
        if input_password!=check_password:
            flask.flash('密碼不一致 請再確認一次')
            return flask.redirect(flask.url_for('register'))
        else:
            msg=register_acc(input_account,input_password)
            if msg=="account is exist!":
                flask.flash('帳號已存在 請換一組帳號')
                return flask.redirect(flask.url_for('register'))
            else:
                flask.flash('註冊已完成 請重新登入')
                return flask.redirect(flask.url_for('login'))
    return flask.render_template('register.html')

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

app.secret_key="Movie-website"
if __name__ == '__main__':
    
    app.run(host='127.0.0.1',port=8000,debug=True)
