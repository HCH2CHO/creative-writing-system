# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 20:10:22 2017

@author: HCHO
"""
import sqlite3

conn=sqlite3.connect('fictData.db')
cur=conn.cursor()

readingfilepath='C:\\Users\\HCHO\\Desktop'
class Apriori(object):
    def __init__(self,readingList):
        self.fictionList=[] #全部文章的列表
        self.readingList=readingList  #子项为列表，“用户名，fiction，fiction，...”
        self.relatedDict={}  #key为列表
    def calculateApriori(self):
        listCount=len(self.readingList)

        for iArtical in self.fictionList:
            for jArtical in self.fictionList:
                if iArtical !=jArtical:
                    itemCount=0
                    intersection=0
                    
                    for k in range(0,listCount):
                        if iArtical in self.readingList[k]:
                            itemCount+=1
                        if iArtical in self.readingList[k] and jArtical in self.readingList[k]:
                            intersection+=1
                            
                    support=intersection/listCount
                    confidence=intersection/itemCount
                    
                    if support>0.2:
                        print (iArtical+'-->'+jArtical,support,confidence)
                        if iArtical not in self.relatedDict:
                            self.relatedDict[iArtical]=[]
                        self.relatedDict[iArtical].append(jArtical)
                        
    def returnDict(self):
        return self.relatedDict

    #relatedDict[iArtical]  即为iArtical的关联文章列表
if __name__ == '__main__':
    relatedList=[]#协同过滤所需的相关文章列表
    with open(readingfilepath) as file:#每行格式为，“用户名，fiction，fiction，...”
        for line in file:
            lineList=line.split(',')
            lineList.pop(0)
            relatedList.append(lineList)
    Apr=Apriori(relatedList)
    Apr.calculateApriori()
    Apr.returnDict()    