#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from ArticutAPI import Articut
from ArticutAPI import ArticutAPI
import json, re, os

def jsonTextReader(jsonFilePath, field):
    with open(jsonFilePath, encoding = "utf-8") as f:
        Content = f.read()
    Content = json.loads(Content)
    return Content[field] 

def jsonFileWriter(jsonDICT, jsonFileName):
    with open(jsonFileName, mode="w") as f:
        json.dump(jsonDICT, f, ensure_ascii=False)
    return None

def DealFolderFile(rootPath):      #處理資料夾中的檔案
    fileLIST = os.listdir(rootPath)#以os.walk指令遞迴搜尋取得檔案列表
    resultDICT = {"reason":[]}
    for file in fileLIST:
        reasonSTR = jsonTextReader(rootPath+'/'+file, "reason")
        #print(reasonSTR) 
        inputDICT = articut.parse(reasonSTR, level = "lv2")
        lawLIST = law(inputDICT)
        
        judgementSTR = jsonTextReader(rootPath+'/'+file, "judgement")
        for i in ("\r\n"):
            judgementSTR = judgementSTR.replace(i, "")        
        #print(judgeSTR)
        inputDICT = articut.parse(judgementSTR, level = "lv2")
        cityLIST = city(inputDICT)
        
        resultDICT = {"law": lawFreqLIST , "city": cityFreqLIST}
        print("讀到字典：{}\n".format(resultDICT)) 
    return resultDICT

def law(inputDICT):
    lawTK = ArticutAPI.LawsToolkit(inputDICT)
    lawLIST = lawTK.getLawArticle() 
    
    for law in lawLIST :
        if (len(law) != 0):
            for data in law:
                found = False
                for i in lawLIST:
                    if i[0] == data[2]:
                        i[1] += 1
                        found = True
                if not found:
                    lawLIST.append([data[2],1])
    lawFreqLIST = []
    for i in lawLIST:
        lawFreqLIST.append((i[0],i[1]))#該法律犯罪緣由第一次出現    
    return lawFreqLIST 

def city(inputDICT):
    tempLIST = articut.getLocationStemLIST(inputDICT)
    cityLIST = []
    for i in tempLIST:
        if i != []: 
            cityLIST.append(i[0][2])  
            
            for city in cityLIST :
                if (len(city) != 0):
                    for data in city :
                        found = False
                        for i in cityLIST:
                            if i[0] == data[2]:
                                i[1] += 1
                                found = True
                        if not found:
                            cityLIST.append([data[2],1])
            cityFreqLIST = []
            for i in cityLIST:
                cityFreqLIST.append((i[0],i[1]))#該城市出現第一次犯罪            
    return cityFreqLIST

def termFreq(inputLIST):
    FreqDICT = {}
    for word in inputLIST:           
        if FreqDICT.get(word):
            FreqDICT[word] = FreqDICT.get(word) + 1
        else:
            FreqDICT[word] = 1 
    return FreqDICT

if __name__== "__main__":
    articut = Articut(username = "nlp2020@droidtown.co", apikey = "yfYwawQRAvuCkPR#W2uug+bpZoN7cEw") 
    rootTUPLE = ("./107刑事", "./106刑事", "./105刑事") 
    print("#107刑事")
    result107 = DealFolderFile(rootTUPLE[0])
    print(result107)
    #print("#106刑事")
    #print(DealFolderFile(rootTUPLE[1]))
    #print("#105刑事")
    #print(DealFolderFile(rootTUPLE[2])) 
    
    MyjsonName1 = "result.json"
    jsonFileWriter(result107, MyjsonName1) 