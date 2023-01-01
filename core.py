import flask
from module import user

app=flask.Flask(__name__)

userManager=user.User('./database/user.sqlite')
print(userManager.isdbconnect)

@app.route('/')
def main():
    return flask.render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if flask.request.method=='GET':
        return flask.render_template('login.html')
    isLogin=userManager.handelUserLogin()
    if not isLogin:
        return flask.redirect('/login')
    else:
        return flask.redirect('/')

app.secret_key="movie-website"
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)
