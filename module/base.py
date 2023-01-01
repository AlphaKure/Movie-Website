import os
import sqlite3
import hashlib


class Base:

    __slots__=['database']

    def __init__(self,databasePath=None) -> None:
        if databasePath:
            self.database=self.databaseConnect(databasePath)

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

