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
        readinglist TEXT)
''')
conn.commit()

