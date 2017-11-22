# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 15:17:52 2017

@author: HCHO
"""
import os

cfile=open("C:\\Users\\HCHO\\Desktop\\all fiction.csv","w")
path="C:\\Users\\HCHO\\Desktop\\creative Writing\\story\\"
for root , dirs, files in os.walk(path):
    try:
        for i in range(0,5):
            path+dirs[i]
            for root1 , dirs1, files1 in os.walk(path+dirs[i]):
                for file in files1: 
                    txt=open(path+dirs[i]+'\\'+file,'r')
                    content=txt.read()
                    cfile.write(content)
    except:
        print ('error')
cfile.close()