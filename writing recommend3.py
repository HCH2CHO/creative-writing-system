# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 20:10:22 2017

@author: HCHO
"""
import sqlite3

conn=sqlite3.connect('history.db')
cur=conn.cursor()

class Apriori(object):
    def __init__(self,readingList):
        self.fictionList=[] #全部文章的列表
        self.readingList=[]  #子项为列表，“用户名，fiction，fiction，...”
        self.relatedDict={}  #key为列表
        
    def readData(self):
        sql_select="SELECT id,readinglist FROM history"
        while True:
            try:                
                cur.execute(sql_select)
                data=cur.fetchone()
                self.readingList.append(data[1].split(','))
                conn.commit()
            except:
                break
        conn.close()
        
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
                            
                    support=intersection/listCount  #i对j的支持度
                    confidence=intersection/itemCount ##i对j的置信度
                    
                    if support>0.2 and confidence>0.5:
                        #print (iArtical+'-->'+jArtical,support,confidence)
                        if iArtical not in self.relatedDict:
                            self.relatedDict[iArtical]=[]
                        self.relatedDict[iArtical].append(jArtical)
                        
    def writeData(self):
        connection=sqlite3.connect('fictData.db')
        cur=connection.cursor()
        for iword in self.relatedDict:
            sql_update="UPDATE fiction SET reArticle={0} WHERE id={1}".format(str(self.relatedDict[iword]),iword)
            cur.execute(sql_update)      
            connection.commit()
        connection.close()

    #relatedDict[iArtical]  即为iArtical的关联文章列表
if __name__ == '__main__':
    Apr=Apriori()
    Apr.calculateApriori()
    Apr.writeData()    
