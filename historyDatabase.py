# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 20:16:31 2017

@author: HCHO
"""

import sqlite3
conn=sqlite3.connect('history.db')
cur=conn.cursor()
cur.execute('''
CREATE TABLE if not exixts history(
        id  TEXT  PRIMARY KEY,
        user TEXT,
        readinglist TEXT)
''')
conn.commit()

for 
    sql_insert="INSERT INTO history VALUES({0},{1})".format(name,string)
    cur.execute(sql_insert)
    conn.commit()
conn.close()