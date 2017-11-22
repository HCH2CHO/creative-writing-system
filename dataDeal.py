# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 09:52:20 2017

@author: HCHO
"""
import math
itm=15

class TFIDF(object):
    def __init__(self):
        self.fictionKeyDict={} #单个文章的词典，子结构为词典
        self.fictionWords={}  #各文章词数量
        self.fictionInfo={}   #value值为列表[TF,IDF,TF*IDF,weight]
        self.cout=0       
        #self.cfile=open('C:\\Users\\HCHO\\Desktop\\fiction KeyWords.csv','r')
        self.cfile=open('C:\\Users\\HCHO\\Desktop\\all.csv','r')
        self.allDict={}  #全部文章的词典
        self.RE={}

    def readFile(self): #将文件1中词频储存在fictionKeyDict中，文章词数储存在fictionWords中
        while True:
            line=self.cfile.readline()
            if line:
                linelist=line.split('!')
                self.fictionKeyDict[linelist[0].strip()]=eval(linelist[5])
                self.fictionWords[linelist[0].strip()]=int(linelist[1])
                self.RE[linelist[0].strip()]=[float(linelist[2]),float(linelist[3]),float(linelist[4])]
                self.cout+=1
            else:
                break
        self.cfile.close()
    
    def  calculateTFIDF(self):
        for iword in self.fictionKeyDict:  #文章名
            for jword in self.fictionKeyDict[iword]:  #词
                if jword not in self.allDict:
                    self.allDict[jword]=1
                else:
                    self.allDict[jword]+=1
        
        TFIDFfile=open('C:\\Users\\HCHO\\Desktop\\fictionTFIDF.csv','w')    
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
             #print (sortline)
             
             #TFIDFfile.write(iword+':'+str(sortline)+'\n')
             #TFIDFfile.write(iword+':'+str(self.fictionInfo[iword])+'\n') 
             sortline=sorted(reDict[iword].items(), key = lambda t:t[1], reverse=True) #按weight排序
             TFIDFfile.write(iword+'!'+str(self.fictionWords[iword])+'!'+str(self.RE[iword][0])+'!'+str(self.RE[iword][1])+'!'+str(self.RE[iword][2])+'!'+str(sortline)+'\n') 
        return reDict
    
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
        
                
class Apriori(object):
    def __init__(self,related0WordDict,iList0):
        self.AprioriDict=related0WordDict
        self.Apriori5List=iList0
    def calculateApriori(self):
        itemCount=len(self.Apriori5List)
        apriDict={}
        #一项子集
        for i in range(0,itm):
            for word in self.Apriori5List[i]:
                wordCount0=0
                '''
                if word not in self.AprioriDict:
                    break
                else:
                    '''
                for j in range(0,itm):
                    if word in self.Apriori5List[j]:
                        wordCount0+=1
                support=wordCount0/itemCount
                print (word,support)
                #二项子集
                if wordCount0>1:
                    apriDict[word]=wordCount0
        
        for iword in apriDict:
            for jword in apriDict:
                wordCount1=0
                if iword !=jword:
                    for k in range(0,itm): 
                        if iword in  self.Apriori5List[k] and jword in self.Apriori5List[k]:
                            wordCount1+=1
                    support=wordCount1/itemCount
                    confidence=wordCount1/apriDict[iword]
                    
                    if support>0.2:
                        print (iword+'-->'+jword,support,confidence)
                                
                       
if __name__ == '__main__':
    ai=TFIDF()
    ai.readFile()
    cosList=ai.calculateTFIDF() #100个词及权重
    articleRE=ai.RE
                             
    for iarticle in cosList:
        for jarticle in cosList:
            if jarticle!=iarticle:
                sim1=cosVector(cosList[iarticle],cosList[jarticle])+0.1*(10-abs(articleRE[iarticle][2]-articleRE[jarticle][2])) #计算相似度
                '''
                if sim1>0.3:
                    print (iarticle,'----',jarticle,sim1)
                    '''
    '''    
    inputArticle=getwords
                    
    for karticle in cosList:
        sim1=cosVector(cosList[karticle],inputArticle)
   '''
   
    #挖掘关联规则
    '''
    relatedWordDict=ai.reAllDict()
    
    #剔除无重复出现词语（不会产生关联规则）
    copyKeys=list(relatedWordDict.keys())
    for relatedWord in copyKeys: 
        if relatedWordDict[relatedWord]<2:
            relatedWordDict.pop(relatedWord)
    
    fictionTxt=list(cosList.keys())  
    iList=[]
    for i in range(6,6+itm): #选取一定的文章
        iList.append(cosList[fictionTxt[i]])
    '''   
    #ap=Apriori(relatedWordDict,iList)
    #ap.calculateApriori()