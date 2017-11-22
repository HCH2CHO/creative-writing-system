# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 18:15:54 2017

@author: HCHO
"""
import re
import string
import operator
import os
import syllables_en

class nGramAlgo(object):

    def __init__(self,fiction):
        self.fiction=fiction  
        self.words=0
        self.ngrams=0
        self.sl=0  #句子的平均单词数
        self.wl=0  #每100个词的平均音节数
        self.RE=0
        
        
    
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

    def returnwords(self):
        return self.words,self.ngrams  #单词数，词频列表
    
    def printwords(self,filepath):
        #filepath.write(file.replace('.txt','')+'!'+str(self.words)+' !'+str(self.RE)+' !'+str(self.ngrams)+'\n') #按格式存储文件名、有用词数、词频
        self.ngrams=sorted(self.ngrams.items(),key = lambda t:t[1],reverse=True)
        filepath.write(file.replace('.txt','')+'!'+str(self.words)+'!'+str(self.wl)+'!'+str(self.sl)+'!'+str(self.RE)+'!'+str(self.ngrams)+'\n')

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
        #print (self.wl,self.sl,self.RE)
        
  
if __name__ == '__main__':
    #content= open('C:\\Users\\HCHO\\Desktop\\Julia Ward Howe.txt','r').read()
    #对本地文件的读取，测试时候用，因为无需联网
    #content = open("1.txt").read()
    #cfile=open("C:\\Users\\HCHO\\Desktop\\fiction KeyWords.csv","w")
    cfile=open("C:\\Users\\HCHO\\Desktop\\all.csv","w")
    sentenceLength={} #用于句子长度统计
    #path="C:\\Users\\HCHO\\Desktop\\creative Writing\\short fictions\\"
    path="C:\\Users\\HCHO\\Desktop\\creative Writing\\all fictions\\"
    for root , dirs, files in os.walk(path):
        for file in files:            
            txt=open(root+'\\'+file,'r')
            content=txt.read()
                                   
            result=nGramAlgo(content)
            result.select150words()
            result.Readablility()
            result.printwords(cfile)
           
            txt.close()            
    cfile.close()       

