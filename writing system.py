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

fictionKeyWordspath='C:\\Users\\HCHO\\Desktop\\fictionKeyWords.csv'
fictionTFIDFpath='C:\\Users\\HCHO\\Desktop\\fictionTFIDF.csv'

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
        return self.ngrams
    
class TFIDF(object):
    def __init__(self):
        self.fictionKeyDict={} #单个文章的词典，子结构为词典
        self.fictionWords={}  #各文章词数量
        self.fictionInfo={}   #value值为列表[TF,IDF,TF*IDF,weight]
        self.cout=0       #项数、文章数
        self.allDict={}  #全部文章词语的词典

    def readFile(self): #将数据库中词频储存在fictionKeyDict中，文章词数储存在fictionWords中       
        sql_select="SELECT id,words,wordfre FROM fiction WHERE TF-IDF is null limit 1;"
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
                     self.fictionInfo[iword].pop(kword[0])
               
             weightAll=0
             for jword in self.fictionInfo[iword]:
                 weightAll+=self.fictionInfo[iword][jword][2]
             for jword in self.fictionInfo[iword]:
                 self.fictionInfo[iword][jword].append(float(100*self.fictionInfo[iword][jword][2]/weightAll))
                 reDict[iword][jword]=self.fictionInfo[iword][jword][3]
    
             sortline=sorted(reDict[iword].items(), key = lambda t:t[1], reverse=True) #按weight排序
             sql_update="UPDATE fiction SET TF-IDF={0} WHERE id={1}".format(str(sortline),iword)
             cur.execute(sql_update)      
             conn.commit()
             
         conn.close()    
         #return reDict
             
    def reAllDict(self):
        return self.allDict
		
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
    

    content="I TOOK a large room, far up Broadway, in a huge old building whose \
    upper stories had been wholly unoccupied for years, until I came. The place \
    had long been given up to dust and cobwebs, to solitude and silence. I seemed \
    groping among the tombs and invading the privacy of the dead, that first night \
    I climbed up to my quarters. "
    result=nGramAlgo(content)
    result.select150words()
    conRE=result.Readablility()
    inputArticle=result.returnwords()  #词频，字典格式  problem

    
    ai=TFIDF()
    ai.readFile()
    cosList=ai.calculateTFIDF() #100个词及权重
    articleRE=ai.RE
    
    articleList=[] #相似文章列表,子列表第一项为文章名
    for karticle in cosList:
        sim1=cosVector(articleList[karticle],inputArticle)+0.1*(10-abs(conRE-articleRE[karticle]))
        articleList.append([karticle,sim1])
    
    ati=sorted(articleList, key =lambda t:t[1], reverse=True)