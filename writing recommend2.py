# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 19:10:40 2017

@author: HCHO
"""

import math
import sqlite3

conn=sqlite3.connect('fictData.db')
cur=conn.cursor()

class TFIDF(object):
    def __init__(self):
        self.fictionKeyDict={} #单个文章的词典，子结构为词典
        self.fictionWords={}  #各文章词数量
        self.fictionInfo={}   #value值为列表[TF,IDF,TF*IDF,weight]
        self.cout=0       #项数、文章数
        self.allDict={}  #全部文章词语的词典

    def readFile(self): #将数据库中词频储存在fictionKeyDict中，文章词数储存在fictionWords中       
        sql_select="SELECT id,words,wordfre FROM fiction;"
        while True:            
            try:
                cur.execute(sql_select)
                data=cur.fetchone()
                conn.commit()
            except:
                break
            self.fictionKeyDict[data[0]]=eval(data[2])
            self.fictionWords[data[0]]=int(data[1])
            self.cout+=1
    
    def  calculateTFIDF(self):
         for iword in self.fictionKeyDict:  #文章名
            for jword in self.fictionKeyDict[iword]:  #词
                if jword not in self.allDict:
                    self.allDict[jword]=1
                else:
                    self.allDict[jword]+=1
        
         reDict={}   #两层字典结构        
         for iword in self.fictionKeyDict:
             self.fictionInfo[iword]={}
             reDict[iword]={}
             
             for jword in self.fictionKeyDict[iword]:
                 #TF,IDF的计算
                 TF=100*self.fictionKeyDict[iword][jword]/self.fictionWords[iword] 
                 IDF=math.log(self.cout)-math.log(self.allDict[jword])
                 self.fictionInfo[iword][jword]=[TF,IDF,TF*IDF]
             #print (self.fictionInfo[iword])
             
             sortTFIDF=sorted(self.fictionInfo[iword].items(), key = lambda t:t[1][2], reverse=True) #按weight排序
             kcout=0
             for kword in sortTFIDF:
                 kcout+=1
                 if kcout >100:
                     self.fictionInfo[iword].pop(kword)
               
             weightAll=0
             for jword in self.fictionInfo[iword]:
                 weightAll+=self.fictionInfo[iword][jword][2]
             for jword in self.fictionInfo[iword]:
                 self.fictionInfo[iword][jword].append(float(100*self.fictionInfo[iword][jword][2]/weightAll))
                 reDict[iword][jword]=self.fictionInfo[iword][jword][3]
    
             sortline=sorted(reDict[iword].items(), key = lambda t:t[1], reverse=True) #按weight排序
             sql_update="UPDATE fiction SET TFIDF={0} WHERE id={1}".format(str(sortline),iword)
             cur.execute(sql_update)      
             conn.commit()
             
         conn.close()    

         #return reDict
             
    def reAllDict(self):
        return self.allDict

if __name__ == '__main__':
    ai=TFIDF()
    ai.readFile()
    ai.calculateTFIDF() #100个词及权重
    
                     