# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 19:32:30 2017

@author: HCHO
"""
import re
import string
import os
import numpy
path="C:\\Users\\HCHO\\Desktop\\short fictions\\"
for root , dirs, files in os.walk(path):
    for file in files:            
        txt=open(path+file,'r')
        content=txt.read()

cont="Her memory was suddenly cut off. She remembered that she had tried to get up and that she was no longer in her bed, that her body had disappeared, that her thirteen favorite books were no longer there, that she was no longer she, now that she was bodiless, floating, drifting over an absolute nothingness, changed into an amorphous dot, tiny, lacking direction. She was unable to pinpoint what had happened. She was confused. She just had the sensation that someone had pushed her into space from the top of a precipice. She felt changed into an abstract, imaginary being. She felt changed into an in corporeal woman, something like her suddenly having entered that high and unknown world of pure spirits. "

fictionTxt=content
sentenceNumList=[0]*40
fictionTxt=fictionTxt.replace('...','.')
fictionList=re.split('[.?!]',fictionTxt)
for sen in fictionList:
    sen.strip(string.punctuation)
    if len(sen.split())<2:
        continue
    else:
        try:
            sentenceNumList[len(sen.split())]+=1
        except:
            print (len(sen.split()))
averageSententh=numpy.average(range(0,40),weights=sentenceNumList)

#方差是否是衡量文章词风的合适参数，有无更好方法
varList
variance=numpy.var(sentenceNumList)