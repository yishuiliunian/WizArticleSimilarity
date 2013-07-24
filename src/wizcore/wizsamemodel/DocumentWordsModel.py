#coding=utf-8
import jieba.posseg as pseg
from decruft import Document
import codecs
import html2text
import math

IgnoreWordsFeatureList = ['w', 'x', 'u', 'p', 'c' ,'q']

def getWordsWeight(wordFeature):
    return 1

    if len(wordFeature) < 1:
        return 0
    if wordFeature[0:1] in IgnoreWordsFeatureList:
        return 0
    return 1

def subTopItemsIndictionary(dic ,length):
    wordMap = dic
    items = sorted(wordMap.items(), key = lambda wordMap:wordMap[1])
    i = 0
    ret = {}
    for item in reversed(items):
        if i >= length:
            break
        i = i + 1
        ret[item[0]] = item[1]
    
    return ret


def topItemsInDictionary(dic ,length):
    wordMap = dic
    items = sorted(wordMap.items(), key = lambda wordMap:wordMap[1])
    i = 0
    topKeys = []
    for item in reversed(items):
        if i >= length:
            break
        i = i + 1
        topKeys.append(item[0])
    return topKeys  

def extractWordCountModel(content):
    words = pseg.cut(content)
    sumCount = 0
    wordMap = {}
    for word in words:
        w = word.word
        if '\n' in w:
            w.replace('\n', '')
        if '\t' in w:
            w.replace('\t', '')
        if len(w.strip()) == 0:
            continue 
        sumCount += 1
        try:
            wordWeight = getWordsWeight(word.flag)
            if wordWeight == 0:
                continue
            if wordMap.has_key(w):
                count = wordMap[w]
                wordMap[w] = count + wordWeight
            else:
                wordMap[w] = wordWeight
            wordMap[w]
        except KeyError:
            continue
    return wordMap, sumCount
 

def extractWordModel(content):
    wrodRatioMap = {}
    wordMap , sumCount = extractWordCountModel(content)
    if sumCount != 0:
        keys = wordMap.keys()
        for key in keys:
            try:
                count = wordMap[key]
                value = float(count)/sumCount
                wrodRatioMap[key] = math.log(float(count)/sumCount)
            except KeyError:
                continue
    return subTopItemsIndictionary(wrodRatioMap, 1000)


def ExtractDocumentCountModel(inputFilePath):
    inFile = codecs.open(inputFilePath, 'r')
    inputData  = inFile.read()
    inFile.close()
    inputStr = Document(inputData).summary()
    contentText = html2text.html2text(inputStr)
    return extractWordCountModel(contentText)
 
def ExtractDocumentRatioModel(inputFilePath):
    inFile = codecs.open(inputFilePath, 'r', 'utf16')
    inputData  = inFile.read()
    inFile.close()
    inputStr = Document(inputData).summary()
    contentText = html2text.html2text(inputStr)
    return extractWordModel(contentText)
    



    
    
    
