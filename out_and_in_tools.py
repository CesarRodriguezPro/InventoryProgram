import sqlite3
import datetime


#  basic configuration


today_date = datetime.datetime.now()
date_only = today_date.strftime('%Y-%m-%d')


def start_connection():

    #  basic set up.
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    return c, conn


#  this are the set of function for the toolsout list inside the database
def created_table_out():
    c, conn = start_connection()
    c.execute('''CREATE TABLE IF NOT EXISTS toolsOut 
    (employeeID TEXT, IBKcode TEXT , date_in TEXT)''')
    c.close()


def tools_out_entry(employeeID, IBKcode,date=today_date):

    c, conn = start_connection()
    created_table_out()  # this will created a table if no created yet
    date_time_now = datetime.datetime.now()  # i have to make this local inside of the code because i didnt work
    c.execute('''INSERT INTO toolsOut
    (employeeID, IBKcode, date_in) VALUES (?,?,?)''',
              (employeeID, IBKcode, date_time_now))
    conn.commit()
    c.close()


def read_from_db_out():
    c, conn = start_connection()
    try:
        c.execute('''SELECT * FROM toolsOut''')
        return c.fetchall()
    finally:
        c.close()


def read_out_report():
    c, conn = start_connection()
    try:
        c.execute("SELECT * FROM toolsOut WHERE date_in > ?", (date_only,))
        return c.fetchall()
    finally:
        c.close()


def name_of_last_employee_with_tools(time_out, code):
    c, conn = start_connection()
    try:
        c.execute("SELECT * FROM toolsOut WHERE date_in >= ? AND IBKcode = ?", (time_out, code))
        return c.fetchone()
    finally:
        c.close()



##########################################################################
#  this are set of function for return list inside the database


def read_from_db_return():
    c, conn = start_connection()
    try:
        c.execute('''SELECT * FROM return''')
        return c.fetchall()
    finally:
        c.close()


def created_table_return():
    c, conn = start_connection()
    c.execute('''CREATE TABLE IF NOT EXISTS return 
    (employeeID text, IBKcode TEXT, date_in TEXT)''')
    c.close()


def tools_return_entry( IBKcode, employeeID):
    c, conn = start_connection()
    created_table_return() # this will created a table if no created yet
    date_time_now = datetime.datetime.now()
    c.execute('''INSERT INTO return
    (employeeID, IBKcode, date_in) VALUES (?,?,?)''',
              (employeeID, IBKcode, date_time_now))
    conn.commit()
    c.close()


def tools_return_entry_no_id(IBKcode):
    c, conn = start_connection()
    created_table_return() # this will created a table if no created yet
    date_time_now = datetime.datetime.now()  # i have to make this local inside of the code because i didn't work
    c.execute('''INSERT INTO return
    (employeeID, IBKcode, date_in) VALUES (?,?,?)''',
              ("None", IBKcode, date_time_now))
    conn.commit()
    c.close()


def read_out_return():
    c, conn = start_connection()
    try:
        c.execute("SELECT * FROM return WHERE date_in >= ?", (date_only,))
        return c.fetchall()
    finally:
        c.close()


if __name__ == '__main__':

    pass
