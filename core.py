import flask
import logging

app=flask.Flask(__name__)


@app.route('/')
def main():
    return flask.redirect(flask.url_for('Home'))

@app.route('/home')
def Home():
    return flask.render_template('home.html')

app.secret_key="movie-website"
if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8000,debug=True)
