# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 18:17:19 2017

@author: HCHO
"""
#collections 和 counter
#problem:关于停词和词频的选择

import re
import string
import operator
import os

class nGramAlgo(object):

    def __init__(self,fiction):
        self.fiction=fiction  
        
    #剔除常用字函数(停词)
    def isCommon(self,ngram):
        commonWords = ["a", "about", "above", "above", "across", "after", "afterwards", 
                       "again", "against", "all", "almost", "alone", "along", "already", 
                       "also","although","always","am","among", "amongst", "amoungst", 
                       "amount",  "an", "and", "another", "any","anyhow","anyone",
                       "anything","anyway", "anywhere", "are", "around", "as",  
                       "at", "back","be","became", "because","become","becomes", 
                       "becoming", "been", "before", "beforehand", "behind", "being", 
                       "below", "beside", "besides", "between", "beyond", "bill", 
                       "both", "bottom","but", "by", "call", "can", "cannot", "cant", 
                       "co", "con", "could", "couldnt", "cry", "de", "describe", 
                       "detail", "do", "done", "down", "due", "during", "each", "eg", 
                       "eight", "either", "eleven","else", "elsewhere", "empty", "enough", 
                       "etc", "even", "ever", "every", "everyone", "everything", 
                       "everywhere", "except", "few", "fifteen", "fify", "fill", 
                       "find", "fire", "first", "five", "for", "former", "formerly", 
                       "forty", "found", "four", "from", "front", "full", "further", 
                       "get", "give", "go", "had", "has", "hasnt", "have", "he", 
                       "hence", "her", "here", "hereafter", "hereby", "herein", 
                       "hereupon", "hers", "herself", "him", "himself", "his", "how", 
                       "however", "hundred", "ie", "if", "in", "inc", "indeed", 
                       "interest", "into", "is", "it", "its", "itself", "keep", 
                       "last", "latter", "latterly", "least", "less", "ltd", "made", 
                       "many", "may", "me", "meanwhile", "might", "mill", "mine", 
                       "more", "moreover", "most", "mostly", "move", "much", "must", 
                       "my", "myself", "name", "namely", "neither", "never", "nevertheless", 
                       "next", "nine", "no", "nobody", "none", "noone", "nor", "not", 
                       "nothing", "now", "nowhere", "of", "off", "often", "on", "once", 
                       "one", "only", "onto", "or", "other", "others", "otherwise", "our", 
                       "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", 
                       "please", "put", "rather", "re", "same", "see", "seem", "seemed", 
                       "seeming", "seems", "serious", "several", "she", "should", "show", 
                       "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", 
                       "someone", "something", "sometime", "sometimes", "somewhere", 
                       "still", "such", "system", "take", "ten", "than", "that", "the", 
                       "their", "them", "themselves", "then", "thence", "there", 
                       "thereafter", "thereby", "therefore", "therein", "thereupon", 
                       "these", "they", "thickv", "thin", "third", "this", "those", 
                       "though", "three", "through", "throughout", "thru", "thus", "to", 
                       "together", "too", "top", "toward", "towards", "twelve", "twenty", 
                       "two", "un", "under", "until", "up", "upon", "us", "very", "via", 
                       "was", "we", "well", "were", "what", "whatever", "when", "whence", 
                       "whenever", "where", "whereafter", "whereas", "whereby", "wherein", 
                       "whereupon", "wherever", "whether", "which", "while", "whither", 
                       "who", "whoever", "whole", "whom", "whose", "why", "will", "with", 
                       "within", "without", "would", "yet", "you", "your", "yours", 
                       "yourself", "yourselves", "the",
                       
                       
                       "a","the","an", 
                       "be","is","are","was","were","been","not","can","would","could","will",
                       "you","it","i","he","she","we",
                       "my","your","her","his","its", "our","their",
                       "me","him","her","they","them","us",
                       "this","that","these","those","here","there",                      
                       "and","but","or","so","if","because","than",  "also", "before",                
                        "of","in","to","with","on","at","from","as","by","about","for","into","up","out",      
                        "what", "who","when", "which","where","how",
                        "i'm","i've","it's","don't",
                        "only","never",
                        
                        "have","has","had", "do","did", "say","said","go","get","got","make","know","give","think","look","take",
                        "see","use", "find","want","like","come", 
                        "one","all","some", "people","man","other","no","many","thing","little",
                        "time","day","month","year", "just","now", "then",   
                        "two",  "first", "new", "more","well","way","good"
                       ]
        
        if ngram in commonWords:
            return True
        else:
            return False
        
    def cleanText1(self):
        fiction = re.sub('\n+', " ", self.fiction).lower() # 匹配换行用空格替换成空格,大写转换成小写
        fiction = re.sub(' +', " ", fiction) #  把连续多个空格替换成一个空格
        fiction = re.sub("‘+"," ",fiction)
        return fiction
    
    def cleanText2(self):
        fiction = self.cleanText1()
        fiction = fiction.split(' ') #以空格为分隔符，返回列表
        cleanInput = []
        for item in fiction:
            item = item.strip(string.punctuation) # string.punctuation获取所有标点符号    
            if len(item) > 1 : #找出单词
                cleanInput.append(item)
        return cleanInput
    
    def getNgrams(self, n):#n为划分词的数量
        fiction = self.cleanText2()
        #print (len(fiction))
        output = {} # 构造字典
        wordNum=0
        for i in range(len(fiction)-n+1):
            ngramTemp = " ".join(fiction[i:i+n])
    
            #if self.isCommon(ngramTemp.split()[0]) or self.isCommon(ngramTemp.split()[1]):
            '''
            if self.isCommon(ngramTemp):   
                pass
            else:
                '''
            wordNum+=1
            if ngramTemp not in output: #词频统计
                output[ngramTemp] = 1 #典型的字典操作
            output[ngramTemp] += 1
        
        #print (wordNum)
        return output,wordNum
    
    def select100words(self):
        self.ngrams,self.words = self.getNgrams(1)
        sortedNGrams = sorted(self.ngrams.items(), key = operator.itemgetter(1), reverse=True) #operator.itemgetter获取某个值 reverse=True 降序排列
        
        count100=1 #计数，取词频最高的100个词
        for num in sortedNGrams:
            if count100>100 or num[1]==2:
                self.ngrams.pop(num[0])
            count100+=1
            '''
            if num[1]<max(5,words/600): #词频筛选条件
                ngrams.pop(num[0])
                #print(num)
        #print (ngrams)
        '''
    def returnwords(self):
        return self.words,self.ngrams
    
    def printwords(self,filepath):
        filepath.write(file.replace('.txt','')+' !'+str(self.words)+' !'+str(self.ngrams)+'\n') #按格式存储文件名、有用词数、词频
        

    #获取核心词在的句子
    '''
    def getFirstSentenceContaining(ngram, content):
        #print(ngram)
        sentences = content.split(".")
        for sentence in sentences:
            if ngram in sentence:
                return sentence
        return ""
    '''

def sentenceCal(fictionTxt): #句子长度向量统计
    sentenceNumList=[0]*30
    fictionTxt=fictionTxt.replace('...','.')
    fictionList=re.split('[.?!]',fictionTxt)
    for sen in fictionList:
        sen.strip(string.punctuation)
        try:
            sentenceNumList[len(sen.split())]+=1
        except:
            print (len(sen.split()))
    
    return sentenceNumList
            
    
    
if __name__ == '__main__':
    #content= open('C:\\Users\\HCHO\\Desktop\\Julia Ward Howe.txt','r').read()
    #对本地文件的读取，测试时候用，因为无需联网
    #content = open("1.txt").read()
    cfile=open("C:\\Users\\HCHO\\Desktop\\fictionKeyWords.csv","w")
    sentenceLength={} #用于句子长度统计
    
    path="C:\\Users\\HCHO\\Desktop\\short fictions\\"
    for root , dirs, files in os.walk(path):
        for file in files:            
            txt=open(path+file,'r')
            content=txt.read()
            
            sentenceLength[file.replace('.txt','')]=sentenceCal(content)
                       
            result=nGramAlgo(content)
            result.select100words()
            result.printwords(cfile)
            
            txt.close()            
    cfile.close()       
    '''
    for top3 in range(3):
        print ("###"+getFirstSentenceContaining(sortedNGrams[top3][0],content.lower())+"###")
    '''