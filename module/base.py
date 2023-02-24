import os
import sqlite3
import hashlib
import flask

class Base:

    __slots__=['database']

    def __init__(self,databasePath=None) -> None:
        if databasePath:
            self.database=self.databaseConnect(databasePath)

    def databaseState(self) -> None:
        if self.database==None: # 出現異常
            flask.flash('資料庫錯誤，請聯繫管理員',category='error')

    @staticmethod
    def databaseConnect(dbPath)->sqlite3.Connection|None:
        if os.path.isfile(dbPath):
            try:
                return sqlite3.connect(dbPath,check_same_thread=False)
            except:
                return None
        return None
    
    @staticmethod
    def hashCal(data:str)->str:
        model=hashlib.sha256()
        model.update(data.encode('utf-8'))
        return model.hexdigest().lower()

