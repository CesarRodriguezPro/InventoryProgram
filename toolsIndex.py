import sqlite3
import datetime


def startconnection():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    return conn, c


def created_table():
    conn, c = startconnection()
    c.execute('''CREATE TABLE IF NOT EXISTS toolIndex 
    (ibkIndex text, typeTool text, brand text, description, serial text, date_in text, job_site text) ''')
    c.close()


def data_entry():
    conn, c = startconnection()
    c.execute('INSERT INTO toolIndex VALUES()')
    c.close()


def dynamic_data_entry(ibkIndex, typeTool, brand, description, serial, job_site):
    conn, c = startconnection()

    created_table()
    #  you need to introduce ibkIndex, typeTool, brand, description, serial, date, job_site
    date = (datetime.datetime.today())
    c.execute('''INSERT INTO toolIndex
    (ibkIndex, typeTool, brand, description, serial, date_in, job_site) VALUES (?,?,?,?,?,?,?)''',
              (ibkIndex, typeTool, brand, description, serial, date, job_site))
    conn.commit()
    c.close()


def read_from_db():
    conn, c = startconnection()
    try:
        c.execute('SELECT * FROM toolIndex')
        x = c.fetchall()
        return x
    finally:
        c.close()


def search_from_db_tool(variable):
    conn, c = startconnection()
    try:
        c.execute('SELECT * FROM toolIndex WHERE ibkIndex =(?)', (variable,))
        return c.fetchone()
    finally:
        c.close()

if __name__ == '__main__':
    pass

   # this is to import data from cvs file to SQLITE
   #
   #  import csv
   #  cvsfile = r'raw_data.csv'
   #
   #  #dynamic_data_entry("test1", 'test2', 'test3', 'test4', 'test5', 'test6')
   #  with open(cvsfile, 'r', newline='') as file_to_read:  # read cvs file and separate files
   #      data_readed = csv.reader(file_to_read)
   #
   #      for x in data_readed:
   #          column1 = x[0]
   #          column2 = x[1]
   #          column3 = x[2]
   #          column4 = x[3]
   #          column5 = x[4]
   #          column6 = x[5]
   #          print('00{:7} {:20}  {:20} {:20} {:20} {}'.format(column1,column2,column3,column4,column5, column6))
   #
   #          #  this is to upload a list of tools in CSV format
   #          #dynamic_data_entry("00"+ column1, column2, column3, column4, column5, column6)
   #      input('Press enter ...')
   #      #c.execute('SELECT * FROM toolIndex')
   #      #for row in c.fetchall():
   #      #     print(row)