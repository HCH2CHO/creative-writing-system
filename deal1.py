# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 19:33:25 2017

@author: HCHO
"""

path="C:\\Users\\HCHO\\Desktop\\all.csv"
cfile=open(path,'r')
myfile=open("C:\\Users\\HCHO\\Desktop\\myall.csv",'w')

while True:
    txt=cfile.readline()
    if txt:
        txt=txt.replace('[','').replace(']','').replace('\n','').replace('(','')
        linelist1=txt.split('!')
        linelist2=linelist1[5].split('),')
        linelist2[-1]=linelist2[-1].replace(')','')
        
        words=''
        for i in linelist2:
            words=words+i+'!'
        myfile.write(str(linelist1[0])+'!'+str(linelist1[1])+'!'+str(linelist1[2])+' !'+str(linelist1[3])+' !'+str(linelist1[4])+' !'+words+'\n')
    else:
        break
