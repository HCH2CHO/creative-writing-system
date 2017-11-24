# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 23:24:10 2017

@author: HCHO
"""

import re
import string
import operator
import math
import syllables_en
import sqlite3

conn=sqlite3.connect('fictData.db')
cur=conn.cursor()

def getAllWords():
    allwordsDict={}
    sql_select="SELECT id,TF-IDF FROM fiction;"
    while True:            
        try:
            cur.execute(sql_select)
            data=cur.fetchone()
            conn.commit()
        except:
            break
        
        for aword in eval(data[1]):  #文章名
            if aword not in allwordsDict:
                allwordsDict[aword]=1
            else:
                allwordsDict[aword]+=1                       
    return allwordsDict

class nGramAlgo(object):
    def __init__(self,fiction):
        self.fiction=fiction  
        self.words=0
        self.ngrams
        self.sl=0  #句子的平均单词数
        self.wl=0  #每100个词的平均音节数
        
    def cleanText(self):
        fiction = re.sub('\n+', " ", self.fiction).lower() # 匹配换行用空格替换成空格,大写转换成小写
        fiction = re.sub(' +', " ", fiction) #  把连续多个空格替换成一个空格
        fiction = re.sub("‘+"," ",fiction)
        
        fiction = fiction.split(' ') #以空格为分隔符，返回列表
        cleanInput = []
        for item in fiction:
            item = item.strip(string.punctuation) # string.punctuation获取所有标点符号    
            if len(item) > 1 : #找出单词
                cleanInput.append(item)
        return cleanInput
    
    def getNgrams(self, n):#n为划分词的数量
        fiction = self.cleanText()
        #print (len(fiction))
        output = {} # 构造字典
                 
        wordNum=len(fiction)
        for i in range(len(fiction)-n+1):
            ngramTemp = " ".join(fiction[i:i+n])
            self.wl+=syllables_en.count(ngramTemp)
            if ngramTemp not in output: #词频统计
                output[ngramTemp] = 1 #典型的字典操作
            output[ngramTemp] += 1
        
        #print (wordNum)
        return output,wordNum
            
    def select150words(self):
        self.ngrams,self.words = self.getNgrams(1)
        sortedNGrams = sorted(self.ngrams.items(), key = operator.itemgetter(1), reverse=True) #operator.itemgetter获取某个值 reverse=True 降序排列
        
        count150=1 #计数，取词频最高的150个词
        for num in sortedNGrams:
            if count150>150 or num[1]==2:
                self.ngrams.pop(num[0])
            count150+=1
    
    def Readablility(self): #易读性公式    
        fictionTxt=self.fiction.replace('...','.')
        fictionList=re.split('[.?!]',fictionTxt)
        #print (len(fictionList))
        i=0
        for sen in fictionList:
            sen.strip(string.punctuation)
            if len(sen.split())<2:
                i=i+1
        self.sl=self.words/(len(fictionList)-i)
        self.wl=self.wl/self.words*100
        self.RE=206.835-0.846*self.wl-1.015*self.sl
        #print (self.wl,self.sl,RE)
        return self.RE
    
    def returnwords(self):
        return self.words,self.ngrams
    
                       
class TFIDF(object):  #该部分可改进，提高速度
    def __init__(self):
        self.cout=0       #项数、文章数
        self.fictionRE={}
        self.fictionKeyDict={} #单个文章的TI-IDF词典，子结构为词典
        self.relatedDict={} #协同过滤获取的文章
        self.reDict={}
        
    def readFile(self): #将数据库中词频储存在fictionKeyDict中，文章词数储存在fictionWords中       
        sql_select="SELECT id,RE,TF-IDF,reArticle FROM fiction;"
        while True:            
            try:
                cur.execute(sql_select)
                data=cur.fetchone()
                conn.commit()
            except:
                break
            self.fictionRE[data[0]]=int(data[1])
            self.fictionKeyDict[data[0]]=eval(data[2])
            self.relatedDict[data[0]]=eval(data[3])
            self.cout+=1
        conn.close()
        
    def getfliter(self):
        return self.relatedDict
    
    def  calculateTFIDF(self):        
         reDict={}   #TF-IDF字典      
         for tword in inputArticle:
             #TF,IDF的计算
             TF=100*inputArticle[tword]/articleWords
             IDF=math.log(self.cout)-math.log(allDict[tword])
             reDict[tword]=TF*IDF
             
         sortTFIDF=sorted(reDict.items(), key = lambda t:t[1], reverse=True) 
         cout=0
         for kword in sortTFIDF:
             cout+=1
             if cout >100:
                 reDict.pop(kword)
           
         weightAll=0
         for jword in reDict:
             weightAll+=reDict[jword]
         for jword in reDict:
             reDict[jword]=float(100*reDict[jword]/weightAll)         
         
         self.reDict= reDict
     
    def getArticle(self):  
        articleList=[] #相似文章列表,子列表第一项为文章名
        for karticle in self.fictionRE:
            sim1=cosVector(self.fictionKeyDict[karticle],self.reDict)
            sim2=0.1*(10-abs(conRE-self.fictionRE[karticle])) #关于可读性的公式存疑
            articleList.append([karticle,sim1,sim2,sim1+sim2])
        return articleList

def cosVector(cosVectorList1,cosVectorList2): #基于空间向量的余弦算法
    numerator=0
    denominator1=0
    denominator2=0
    for word1 in cosVectorList1:
        if word1 in cosVectorList2:
            numerator+=cosVectorList1[word1]*cosVectorList2[word1]            
        denominator1+=cosVectorList1[word1]*cosVectorList1[word1]
        
    for word2 in cosVectorList2:
        denominator2+=cosVectorList2[word2]*cosVectorList2[word2]
        
    similiarity=numerator/(math.sqrt(denominator1)*math.sqrt(denominator2))
    return similiarity

    
if __name__ == '__main__':
    allDict={}
    allDict=getAllWords()
            
    ai=TFIDF()
    ai.readFile()
    recommend2=ai.getfliter() #2为协同过滤推荐(数量不定),结构为字典-列表
    
    content="I TOOK a large room, far up Broadway, in a huge old building whose \
    upper stories had been wholly unoccupied for years, until I came. The place \
    had long been given up to dust and cobwebs, to solitude and silence. I seemed \
    groping among the tombs and invading the privacy of the dead, that first night \
    I climbed up to my quarters. "
    
    result=nGramAlgo(content)
    result.select150words()
    conRE=result.Readablility()
    articleWords,inputArticle=result.returnwords()  #词频，字典格式  problem
    
    ai.calculateTFIDF() #输入文本的100个词及权重
    recommend1=ai.getArticle() #1为词频分析推荐
    
    at1=sorted(recommend1, key =lambda t:t[3], reverse=True)