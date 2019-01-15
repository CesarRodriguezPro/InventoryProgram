import sqlite3


#  this is just to make easy to import data to database

def start_connection():
    #  basic set up.

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    return c, conn


def data_entry():
    c, conn = start_connection()
    c.execute('INSERT INTO EmployeeIndex VALUES()')
    c.close()


def dynamic_data_entry(name, timecode, card_number):
    c, conn = start_connection()
    #  you need to introduce ibkIndex, typeTool, brand, description, serial, date, job_site
    c.execute('''INSERT INTO EmployeeIndex 
    (Name, 
    TimestationCode, 
    card_number) VALUES (?,?,?)''', (name, timecode,card_number))
    conn.commit()
    c.close()


def read_from_db():
    c, conn = start_connection()
    c.execute('SELECT * FROM EmployeeIndex')
    for row in c.fetchall():
        print(row)
    c.close()


def search_from_db_employee(variable):
    c, conn = start_connection()
    try:
        c.execute('SELECT * FROM EmployeeIndex WHERE TimestationCode = ?', (variable,))
        return c.fetchone()
    finally:
        c.close()


def search_from_db_employee_name(variable):

    c, conn = start_connection()
    try:
        c.execute('SELECT * FROM EmployeeIndex WHERE Name =(?)', (variable,))
        return c.fetchone()
    finally:
        c.close()


def search_by_card_number(code):
    c, conn = start_connection()
    try:
        c.execute('SELECT * FROM EmployeeIndex WHERE card_number =(?)', (code,))
        return c.fetchall()
    finally:
        c.close()

if __name__ == '__main__':
    print('This is a associated file for the GUI_Main. to activate the program please click Gui_Main.pyw')


    #  this is to import data from cvs file to SQLITE
    
    # import csv
    # cvsfile = 'database\Employees_Codes.csv'
    #
    # with open(cvsfile, 'r', newline='') as file_to_read:  # read cvs file and separate files
    #     data_readed = csv.reader(file_to_read)
    #
    #     for x in data_readed:
    #         column1 = x[0]
    #         column2 = x[1]
    #         column3 = x[2]
    #         column4 = x[3]
    #         column5 = x[4]
    #         column6 = x[5]
    #         dynamic_data_entry(column2, column3)
    #
    # x = search_from_db('8101372817502270351988442196240')
    # print(x)
    # read_from_db()

