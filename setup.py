import sqlite3
import configparser
from module.base import Base


def setupcheck()->bool:
    config=configparser.ConfigParser()
    config.read('./setting.ini')


def userDBCreate():
    userDB=sqlite3.connect('./database/user.sqlite')
    userDB.cursor()
    userDB.execute('CREATE TABLE IF NOT EXISTS account(username TEXT NOT NULL PRIMARY KEY,password TEXT NOT NULL,isAdmin INTEGER NOT NULL )')
    userDB.commit()

def addAdminaccount(username,password):
    userDB=sqlite3.connect('./database/user.sqlite')
    userDB.cursor()
    userDB.execute('INSERT INTO account VALUES(?,?,1)',(username,password))
    userDB.commit()

if __name__=='__main__':
    adminUsername=input('Username:')
    adminPassword=Base.hashCal(input('Password:'))
    addAdminaccount(adminUsername,adminPassword)