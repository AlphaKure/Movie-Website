import sqlite3

userdb=sqlite3.connect('./database/user.sqlite').cursor()
#userdb.execute('CREATE TABLE userdata(username TEXT,password TEXT)')