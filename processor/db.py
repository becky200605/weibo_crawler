import pymysql
from etc.settings import DB_CONFIG

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            port=DB_CONFIG['port'],
            charset='utf8mb4',
        )
        self.cursor = self.connection.cursor()

    def execute(self, query, params=None):
        self.cursor.execute(query, params)
        self.connection.commit()
    
    def execute_many(self, query, params_list):
        self.cursor.executemany(query, params_list)
        self.connection.commit()

    def fetch_one(self,sql,params=None):
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchone()

    def fetch_all(self,sql,params=None):
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()