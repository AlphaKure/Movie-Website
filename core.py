import flask
import ujson
from check import check
from register import register_acc
from ticket import ticketjson_gen

app=flask.Flask(__name__)

@app.template_global()
def getcookie():
    return True if flask.request.cookies.get('logged_in') == "Y" else False

@app.route('/')
def main():
    return flask.redirect(flask.url_for('Home'))

@app.route('/home')
def Home():
    return flask.render_template('home.html')

@app.route('/future')
def future():
    return flask.render_template('come_soon.html')

@app.route('/ticketln',methods=["POST","GET"])
def ticketln():
    if flask.request.cookies.get('logged_in') != "Y":
        return flask.redirect(flask.url_for('login'))
    else:
        if flask.request.method=='POST':
            nowuser=flask.request.cookies.get('nowuser')
            ticketjson_gen(nowuser)
            return flask.redirect(flask.url_for('Home'))
        return flask.render_template('ticketln.html')

@app.route('/login',methods=["POST","GET"])
def login():
    if flask.request.method=='POST':
        input_account=flask.request.values.get('Username')
        input_password=flask.request.values.get('Password')
        if check(input_account,input_password,"user"):
            resp = flask.make_response(flask.redirect('/home'))
            resp.set_cookie('logged_in',"Y",expires=None)
            resp.set_cookie('nowuser',input_account,expires=None)
            return resp
        else:
            flask.flash('登入失敗 請確認帳號和密碼')
    return flask.render_template('login.html')

@app.route('/logout')
def logout():
    resp = flask.make_response(flask.redirect('/home'))
    resp.set_cookie('logged_in',"N",expires=0)
    resp.set_cookie('nowuser',"",expires=None)
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

@app.route('/movie1')
def movie1():
    return flask.render_template('movie1.html')

@app.route('/movie2')
def movie2():
    return flask.render_template('movie2.html')

@app.route('/Adminlogin',methods=["POST","GET"])
def Adminlogin():
    isAdmin=flask.request.cookies.get('isAdmin')
    if isAdmin=='Y':
        return flask.redirect(flask.url_for('Dashboard'))
    else:
        if flask.request.method == 'POST':
            input_account=flask.request.values.get('account')
            input_password=flask.request.values.get('password')
            isAdmin=check(input_account,input_password,"Admin")
            if isAdmin==True:
                resq=flask.make_response(flask.redirect('/Dashboard'))
                resq.set_cookie('isAdmin','Y',expires=None)
                return resq
            else:
                return flask.render_template('Adminlogin.html',ERROR='管理員帳號或密碼錯誤')
        return flask.render_template('Adminlogin.html')

@app.route('/Dashboard',methods=["POST","GET"])
def Dashboard():
    isAdmin=flask.request.cookies.get('isAdmin')            
    if isAdmin=='Y':
        return flask.render_template('Dashboard.html')
    else:
        return "You don't have Authority!"

@app.route('/Adminlogout')
def Adminlogout():
    isAdmin=flask.request.cookies.get('isAdmin')
    if isAdmin=='Y':
        resq=flask.make_response(flask.redirect('/Adminlogin'))
        resq.set_cookie('isAdmin','N',expires=None)
        return resq
    else:
        return flask.redirect('/Adminlogin')

@app.route('/getjson/<dataname>')
def getjson(dataname):
    isAdmin=flask.request.cookies.get('isAdmin')
    if isAdmin=='Y':
        with open('data/'+dataname+'.json','r',encoding='utf-8')as f:
            data=ujson.load(f)
            f.close()
        return flask.jsonify(data)
    else:
        return flask.redirect('/Adminlogin')

app.secret_key="Movie-website"
if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8000,debug=True)
