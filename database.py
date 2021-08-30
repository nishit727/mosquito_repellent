import sqlite3
from sqlite3 import Error
import time
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        password text NOT NULL
                                    ); """

sql_create_mosquitoes_table = """CREATE TABLE IF NOT EXISTS mosquitoes (
                                    id integer PRIMARY KEY,
                                    date integer NOT NULL,
                                    device_id text NOT NULL,
                                    specie integer
                                );"""

db_name = "mosquito.db"
secret_key = "my secret key"

class Database:

    def __init__(self):
        self.conn = self.create_connection(db_name)
        if self.conn:
            self.create_tables()

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn

    def create_tables(self):
        self.create_table(sql_create_users_table)
        self.create_table(sql_create_mosquitoes_table)

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            cur = self.conn.cursor()
            cur.execute(create_table_sql)
        except Error as e:
            print(e)

    def add_user(self, name, password):
        """ Add a new user into the users table
        :param name:
        :param password_hashed:
        :return: boolean
        """
        try:
            password_hashed = pwd_context.encrypt(password)
            print(password_hashed)
            sql = ''' INSERT INTO users(name,password)
                                  VALUES(?,?) '''
            cur = self.conn.cursor()
            cur.execute(sql, (name, password_hashed,))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def add_mosquito(self, date, device_id, specie):
        """ Add a new mosquito detection into the mosquitoes table
        :param date:
        :param device_id:
        :param specie:
        :return: boolean
        """
        print(date, device_id, specie)
        try:
            sql = ''' INSERT INTO mosquitoes(date,device_id,specie)
                                  VALUES(?,?,?) '''
            cur = self.conn.cursor()
            cur.execute(sql, (date, device_id, specie,))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_mosquito_by_date_range(self, start_date, end_date):
        """
        Get mosquitoes by date range
        :param start_date:
        :param end_date:
        :return: list of mosquitoes
        """
        if start_date is None:
            start_date = 1
        if end_date is None:
            end_date = int(time.time())
        try:
            sql = ''' SELECT date, device_id, specie FROM mosquitoes WHERE date>? AND date<?'''
            cur = self.conn.cursor()
            cur.execute(sql, (start_date, end_date,))
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print(e)
            return None

    def verify_user(self, name, password):
        """
        Get user details by name
        :param name:
        :param password:
        :return: boolean
        """
        if name is None:
            return None
        try:
            sql = ''' SELECT password FROM users WHERE name=?'''
            cur = self.conn.cursor()
            cur.execute(sql, (name,))
            rows = cur.fetchall()
            if rows is not None and len(rows) >= 1:
                hashed_password = rows[0][0]
                return pwd_context.verify(password, hashed_password)
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def user_exits(self, name):
        """

        :param name:
        :return:
        """
        if name is None:
            return None
        try:
            sql = ''' SELECT * FROM users WHERE name=?'''
            cur = self.conn.cursor()
            cur.execute(sql, (name,))
            rows = cur.fetchall()
            if rows is not None and len(rows) == 1:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def generate_token(self, username, expires_in=600):
        s = Serializer(secret_key, expires_in=expires_in)
        token = str(s.dumps({'username': username}))
        return token[token.find("\'") + 1:token.rfind("\'")]

    def verify_token(self, token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
            username = data['username']
            return self.user_exits(username)
        except SignatureExpired:
            return False, "token expired"
        except BadSignature:
            return False, "invalid token"
