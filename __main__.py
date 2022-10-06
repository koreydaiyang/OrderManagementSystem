import os
import sys
sys.path.append(os.getcwd())
from dotenv import load_dotenv
from MainPages import *
import pymysql
load_dotenv()
MY_SQL_PASSWORD = os.getenv('MY_SQL_PASSWORD')
SQL_FILE = os.getenv('SQL_FILE')
DB_NAME = os.getenv('DB_NAME')
USERNAME = 'root'

def checkSQL():
    conn = pymysql.connect(host='localhost', port=3306, user=USERNAME, password=MY_SQL_PASSWORD, charset='utf8')
    readSQLFile(SQL_FILE, conn)
    conn.close()

def readSQLFile(filename, conn):
    cursor = conn.cursor()
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')

    for command in sqlCommands:
        if command.strip() != '':
            cursor.execute(command)
            conn.commit()

if __name__ == "__main__":
    checkSQL()
    Main_Page().mainloop()