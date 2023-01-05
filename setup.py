import sqlite3
import configparser
from module.base import Base


def setupCheck()->bool:
    config=configparser.ConfigParser()
    config.read('./setting.ini')


def userDBCreate():
    userDB=sqlite3.connect('./database/user.sqlite')
    userDB.cursor()
    userDB.execute('CREATE TABLE IF NOT EXISTS account(username TEXT NOT NULL PRIMARY KEY,password TEXT NOT NULL,email TEXT NOT NULL,nickname TEXT,isAdmin INTEGER NOT NULL)')
    userDB.commit()

def addAdminAccount(username,password,email,nickname):
    userDB=sqlite3.connect('./database/user.sqlite')
    userDB.cursor()
    userDB.execute('INSERT INTO account VALUES(?,?,?,?,1)',(username,password,email,nickname))
    userDB.commit()

if __name__=='__main__': 
    adminUsername=input('Username:')
    adminPassword=Base.hashCal(input('Password:'))
    adminEmail=input('Email:')
    adminNickname=input('nickname:')
    addAdminAccount(adminUsername,adminPassword,adminEmail,adminNickname)