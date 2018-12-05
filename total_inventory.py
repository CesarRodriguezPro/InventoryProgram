import sqlite3
import datetime
from collections import Counter

conn = sqlite3.connect('database.db')
c = conn.cursor()


def read_from_db():
    c.execute('SELECT * FROM toolIndex')
    x = c.fetchall()
    return x


def total_inventory_count():

    p = read_from_db()
    list =[]
    for x in p:
        location = x[6]
        type_tool = x[1]
        location = location.lower()
        if location == "123 linden":
            list.append(type_tool.lower().strip())

    p = Counter(list)
    return p

if __name__ == '__main__':
    p = total_inventory_count()
    for key in p:
        print(" {:20}   {} ".format(key, p[key]))
    input('press enter')