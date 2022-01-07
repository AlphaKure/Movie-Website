import flask
from check import check

app=flask.Flask(__name__)

isAdmin=False

@app.route('/')
def main():
    return flask.redirect(flask.url_for('login'))

@app.route('/login',methods=["POST","GET"])
def login():
    if flask.request.method == 'POST':
        input_account=flask.request.values.get('account')
        input_password=flask.request.values.get('password')
        global isAdmin
        isAdmin=check(input_account,input_password)
        return flask.redirect(flask.url_for('Dashboard'))
        
    return flask.render_template('login.html')

@app.route('/Dashboard')
def control():
    if isAdmin:
        return "Welcome!"
    else:
        return "You don't have Authority!"
        


if __name__ == '__main__':
     app.run(host='127.0.0.1',port=8000,debug=True)
