import sqlite3
import datetime
import out_and_in_tools
''' this is just of set of funtion to be used in the Windows_main  or Linux_main
all of this function are design to manage the missing tools options and properties
i decide to separate because of it was easier to text and manege as we update program.'''


today_date = datetime.date.today()
#today_date = '2018-05-15'


def start_connection():

    #  basic set up.
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS missing_tools 
    (employee text, IBKcode, date_in)''')
    conn.commit()
    return c, conn


def last_date():

    '''
    this function search in to the tools out and looks for the last date in which we work and
    uses that date as reference to determent when its consider missing tools or just in to the range of
    return . return tools is consider open during the whole present day but missing tools is consider to be
    from yesterday date or before ( think about friday)
    '''

    c, conn = start_connection()
    c.execute("SELECT date_in FROM toolsOut where date_in < ? ", (today_date,))
    x = c.fetchall()
    d = datetime.datetime.strptime(x[-1][0], '%Y-%m-%d %H:%M:%S.%f')
    date_to_return = d.date()

    return date_to_return


def time_convertion(time_convert):

    try:
        return datetime.datetime.strptime(str(time_convert), '%Y-%m-%d %H:%M:%S.%f')
    except:
        return datetime.datetime.strptime(time_convert , '%Y-%m-%d %H:%M:%S.%f')


def search_for_missing_just_tools(data_out, data_return):

    def convert_time_regular(time_convert):
        return time_convert.strftime('%Y-%m-%d %H:%M:%S')

    tools_out = {}
    for name, code, timestamp in data_out:
        key = code

        if key not in tools_out or tools_out[key] < time_convertion(timestamp):
            tools_out[key] = time_convertion(timestamp)

    tools_return = {}
    for name, code, timestamp in data_return:
        key = code
        if key not in tools_return or tools_return[key] < time_convertion(timestamp):
            tools_return[key] = time_convertion(timestamp)

    missing_list = []
    for items in tools_out:
        if items not in tools_return or tools_return[items] < tools_out[items]:
            missing_list.append([items, convert_time_regular(tools_out[items])])

    return missing_list


def search_for_missing(data_out, data_return):

    '''
    this is to search inside the database and find the unique item that are not in both list
    also check to see if the dates of the tool bring back are not later of the returns. just in case
    the same employee check for the same tool multiple times in the same day.
    '''

    tools_out = {}
    for name, code, timestamp in data_out:
        key = name, code
        if key not in tools_out or tools_out[key] < time_convertion(timestamp):
            tools_out[key] = time_convertion(timestamp)


    tools_return = {}
    for name, code, timestamp in data_return:
        key = name, code
        if key not in tools_return or tools_return[key] < time_convertion(timestamp):
            tools_return[key] = time_convertion(timestamp)


    for items in tools_out:
        if items not in tools_return or tools_return[items] < tools_out[items]:
            print('{}  {}'.format(items, tools_out[items]))


def missing_tools_previous():

    '''
    basic report for previous day
    '''

    c, conn = start_connection()
    x = last_date()
    previous_date = x
    try:
        c.execute("SELECT * FROM toolsOUt WHERE date_in > ? and date_in < ?", (previous_date, today_date))
        data_out = c.fetchall()
        c.execute("SELECT * FROM return WHERE date_in > ? and date_in < ?", (previous_date, today_date))
        data_return = c.fetchall()
        x = search_for_missing_just_tools(data_out, data_return)
        return x
    except:
        c.close()


def missing_tools_total():

    '''
    basic report for all from the beginning of time.
    '''

    c, conn = start_connection()
    try:
        c.execute("SELECT * FROM toolsOUt ")
        data_out = c.fetchall()

        c.execute("SELECT * FROM return")
        data_return = c.fetchall()

        x = search_for_missing_just_tools(data_out, data_return)
        return x
    except:
        c.close()


def missing_tools_current():
    c, conn = start_connection()
    try:
        c.execute("SELECT * FROM toolsOUt WHERE date_in > ?", (today_date,))
        data_out = c.fetchall()

        c.execute("SELECT * FROM return WHERE date_in > ? ", (today_date,))
        data_return = c.fetchall()

        x = search_for_missing_just_tools(data_out, data_return)

        return x
    finally:
        c.close()


def check_for_doubles(c, conn, employee, IBKcode, date_in):

    c.execute('''SELECT * FROM missing_tools
     WHERE employee =?  AND 
     IBKcode = ? AND
     date_in = ? ''', (employee, IBKcode, date_in))
    x = c.fetchall()

    if len(x) == 0:
        return True
    else:
        return False


def created_report_for_missing_tools():

    c, conn = start_connection()
    data = missing_tools_current()
    for row in data:
        code = row[0]
        timestamp = row[1]
        name_info = out_and_in_tools.name_of_last_employee_with_tools(timestamp, code)
        x = check_for_doubles(c, conn,name_info[0], code, timestamp)
        if x:
            c.execute('''INSERT OR IGNORE INTO missing_tools
            (employee, IBKcode, date_in) VALUES (?,?,?)''', (name_info[0], code, timestamp))
        else:
            pass
    conn.commit()
    c.close()


def created_report_for_missing_tools_previous():
    c, conn = start_connection()
    data = missing_tools_previous()
    for row in data:
        code = row[0]
        timestamp = row[1]
        name_info = out_and_in_tools.name_of_last_employee_with_tools(timestamp, code)
        x = check_for_doubles(c, conn,name_info[0], code, timestamp)
        if x:
            c.execute('''INSERT OR IGNORE INTO missing_tools
            (employee, IBKcode, date_in) VALUES (?,?,?)''', (name_info[0], code, timestamp))
        else:
            pass

    conn.commit()
    c.close()


def read_missing_tools():
    c, conn = start_connection()
    c.execute("SELECT * FROM missing_tools")
    x = c.fetchall()
    c.close()
    return x


def delete_from_missing(code):
    c, conn = start_connection()
    c.execute("DELETE FROM missing_tools WHERE IBKcode = ? ", (code,))
    conn.commit()
    c.close()


if __name__ == '__main__':
    x = missing_tools_current()
    for item in x:
        print(item[0])


