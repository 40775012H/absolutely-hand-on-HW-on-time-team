#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from ArticutAPI import Articut
import json, re, os

def jsonTextReader(jsonFilePath, field):
    with open(jsonFilePath, encoding = "utf-8") as f:
        Content = f.read()
    Content = json.loads(Content)
    return Content[field] 


def STR2sentence(inputSTR):#將字串斷句的程式               
    BlankMark = [" ", "...","…", "「", "」", "\r", "\n", "\u3000"]
    CutMark = ["，", "。", "：", "（", "）"]
    LastMark = ["<MyCuttingMark><MyCuttingMark><MyCuttingMark>", "<MyCuttingMark><MyCuttingMark>"]

    for i in BlankMark:
        inputSTR = inputSTR.replace(i, "")
    for j in range (len(inputSTR)):
        if inputSTR[j] == ",":
            if re.match( r"[0-9],[0-9]", inputSTR[j-1:j+2]):
                pass
            else:
                inputSTR = inputSTR[:j] + "<MyCuttingMark>" + inputSTR[j+1:]
    for k in CutMark:
        inputSTR = inputSTR.replace(k, "<MyCuttingMark>")
    for m in LastMark:
        inputSTR = inputSTR.replace(m, "<MyCuttingMark>")
    inputLIST = inputSTR.split("<MyCuttingMark>")

    return inputLIST

def termFreq(inputLIST):
    result = {}
    for word in inputLIST:           
        if result.get(word):
            result[word] = result.get(word) + 1
        else:
            result[word] = 1 
    return result 

def termFreq_1(inputLIST):
    global articut
    result = {"宜蘭":0, "花蓮":0, "臺東":0, "基隆":0, "臺北":0, "新北":0, "桃園":0, "新竹":0, "苗栗":0, "臺中":0, "南投":0, "彰化":0, "雲林":0, "嘉義":0, "臺南":0, "高雄":0, "屏東":0}
    item = ["宜蘭", "花蓮", "臺東", "基隆", "臺北", "新北", "桃園", "新竹", "苗栗", "臺中", "南投", "彰化", "雲林", "嘉義", "臺南", "高雄", "屏東"]
  
    for sentence in inputLIST: 
         #    = articut.parse(sentence, level = "lv2")        
        if "宜蘭" not in sentence:
            result["宜蘭"] += 0
        else:
            result["宜蘭"] += 1        
        if "花蓮" not in sentence:
            result["花蓮"] += 0
        else:
            result["花蓮"] += 1         
        if "臺東" not in sentence:
            result["臺東"] += 0
        else:
            result["臺東"] += 1        
        if "基隆" in sentence:
            result["基隆"] += 1
        else:
            result["基隆"] += 0 
        if "臺北" in sentence:
            result["臺北"] += 1
        else:
            result["臺北"] += 0   
        if "新北" in sentence:
            result["新北"] += 1
        else:
            result["新北"] += 0  
        if "桃園" in sentence:
            result["桃園"] += 1
        else:
            result["桃園"] += 0         
        if "新竹" in sentence:
            result["新竹"] += 1
        else:
            result["新竹"] += 0     
        if "苗栗" in sentence:
            result["苗栗"] += 1
        else:
            result["苗栗"] += 0 
        if "高雄" in sentence:
            result["高雄"] += 1
        else:
            result["高雄"] += 0 
    return result

def DealFolderFile(rootPath):      #處理資料夾中的檔案
    fileLIST = os.listdir(rootPath)#以os.walk指令遞迴搜尋取得檔案列表
    lawDICT = {"reason":[]}
    for file in fileLIST:
        reasonSTR = jsonTextReader(rootPath+'/'+file, "reason")
        print(reasonSTR)        
        judgeSTR = jsonTextReader(rootPath+'/'+file, "judgement")
        #print(judgeSTR)
        inputDICT = articut.parse(judgeSTR, level = "lv2", openDataPlaceAccessBOOL = True)
        temp = articut.getLocationStemLIST(inputDICT)
        locLIST = []
        if(temp != None):
            for i in temp:
                if i != [] and i[0][2] not in locLIST: 
                    locLIST.append(i[0][2])  
                    
        #opinionSTR = jsonTextReader(rootPath+'/'+file, "opinion")
        lawDICT["reason"].append(STR2sentence(reasonSTR))
        #lawDICT["city"].append(locLIST)
        #print(STR2sentence(judgeSTR)) 
        #lawDICT["city"].append(STR2sentence(opinionSTR))
        
        cityCountLIST = termFreq(locLIST)  
        lawDICT["city"] = cityCountLIST
       
    return lawDICT#純粹只有算犯罪總案件數

def jsonFileWriter(jsonDICT, jsonFileName):
    with open(jsonFileName, mode="w") as f:
        json.dump(jsonDICT, f, ensure_ascii=False)
    return None

if __name__== "__main__":
    articut = Articut(username = "nlp2020@droidtown.co", apikey = "yfYwawQRAvuCkPR#W2uug+bpZoN7cEw") 
    rootTUPLE = ("./107刑事", "./106刑事", "./105刑事") 
    print("#107刑事")
    result = DealFolderFile(rootTUPLE[0])
    print(result)
    #print("#106刑事")
    #print(DealFolderFile(rootTUPLE[1]))
    #print("#105刑事")
    #print(DealFolderFile(rootTUPLE[2])) 
    
    MyjsonName1 = "result_2.json"
    jsonFileWriter(result, MyjsonName1) 
    #print("讀到字典：{}\n".format(result)) 
    