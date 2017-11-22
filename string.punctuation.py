# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 12:34:17 2017

@author: HCHO
"""

import string
list = ['a,','b!','cj!/n']
item=[]
for i in list:
    i =i.strip(string.punctuation)
    item.append(i)
print (item)