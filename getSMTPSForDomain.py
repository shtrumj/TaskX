from taskManager.models import Users, Customers, Employees, Tasks, WorkReports
import sqlite3
import os
import ldap

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

db_file= (os.path.join(os.getcwd() ,"data.sqlite3"))
create_connection(db_file)

def get_customers_ext_domain(conn):
    cur = conn.cursor()
    cur.execute("SELECT externalDomain FROM customers")
    rows = cur.fetchall()
    for row in rows:
        print(row)
