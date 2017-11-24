# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 13:21:34 2017

@author: HCHO
"""

import sqlite3
def convert(value):
    if value.startwith('~'):
        return value.strip('~')
    if not value:
        value='0'
    return float(value)

conn=sqlite3.connect('food.db')
curs=conn.cursor()

curs.execute('''
CREATE TABLE food(
        id  TEXT  PRIMARY KEY
        desc TEXT,
        water FLOAT,
        kcal FLOAT,
        protein FLOAT,
        fat FLOAT,
        ash FLOAT,
        carbs FLOAT,
        fiber FLOAT,
        sugar FLOAT)
''')

query='INSERT INTO food VALUES(?,?,?,?,?,?,?,?,?,?)'

for line in open('ABBREV.txt'):
    fields=line.split('^')
    vals=[convert(f) for f in fields]
    curs.execute(query.vals)
    
conn.commit()
conn.close()

import sqlite3, sys
conn=sqlite3.connect('food.db')
curs=conn.cursor()

query='SELECT *FROM food WHERE %s' % sys.argv[1]
print (query)
curs.execute(query)
names=[f[0] for f in curs.description]
for row in curs.fetchall():
    for pair in zip(names, row):
        print ('%s:%s' %pair)
    print