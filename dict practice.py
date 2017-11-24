# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 12:48:22 2017

@author: HCHO
"""

d = {
 'Adam': 95, #key : value
 'Lisa': 85,
 'Bart': 59
 }

#d={}
d['Paul'] = 72 
if 'Adam' in d:
    print (d['Adam'])
    
print (d.get('Bart'))

d['Paul'] = 72 
 
d.pop('Paul')

#d.clear()

for key in d:
    print (key,'-',d[key])

print (d['Bart'])

print(d.items())