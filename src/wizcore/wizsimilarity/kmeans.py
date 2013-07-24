#coding=utf-8
import math
import pdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import vimpdb
import copy
import pickle
import random
from wizfile import DocumentAllModelsPath 
def ConvertCN(s):
    try:
        return s.decode('utf-8').encode('utf-8')
    except:
        return s
KeyCharOfFileSplit = '\t'
KeyCharOfStrSplit = ':'
DocumentList = []
ClassModelList =[]

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


def maxItemInDictionary(dic, length):
    wordMap = dic
    items = sorted(wordMap.items(), key = lambda wordMap:wordMap[1])
    tempCenter = {}
    i = 0
    for item in reversed(items):
        if i >= length:
            break
        tempCenter[item[0]] = item[1]
        i = i + 1
    return tempCenter


import os
import codecs
removeWordsList = ['gif','index',u'和','jpg','1','3','com','4','10', u'了',u'在', u'是' ,'10','2',u'后', u'的', 'place', 'nbsp', 'holder','png','files','http']
def initData(dataFilePath, numberOfKinds, makStepCount):

    global ClassModelList
    wordsMap = {}
    i = 0
    documents = os.listdir(dataFilePath)
    docLength = len(documents)
    print docLength
    randomSeed = len(documents) / numberOfKinds
    totalKindModelCount = 0
    for doc in documents:
        if doc.endswith('Store'):
            continue
        filePath = dataFilePath + '/' +doc
        sfile = codecs.open(filePath, 'r')
        from wizsamemodel import DocumentModel
        dModel = pickle.load(sfile)
        sfile.close()
        documentDataMap = dModel.wordsCountMap
        for w in removeWordsList:
            if w in documentDataMap:
                documentDataMap.pop(w)
        documentTitle = doc
        document = Document(documentTitle, documentDataMap)
        if random.randint(0,docLength) % randomSeed == 0:
            if totalKindModelCount < numberOfKinds:
                kindModel = ClassModel(document)
                ClassModelList.append(kindModel)
                totalKindModelCount += 1

        DocumentList.append(document)
        i += 1
    stepCount = 0
    while stepCount < makStepCount:
        for kind in ClassModelList:
            kind.clearDocumentList()
        for doc in DocumentList:
            maxDistance = 10000000000
            maxDistanceIndex = 0
            k = 0
            for kind in ClassModelList:
                center = kind.center
                distance = doc.distance(center)
                if distance < maxDistance:
                    maxDistance = distance
                    maxDistanceIndex =  k
                k += 1
            kind = ClassModelList[maxDistanceIndex]
            kind.addDocument(doc)
        sumStepLength = 0.0
        for kind in ClassModelList:
            kind.calAvarageCenter()
            currentDistance = kind.center.distance(kind.lastCenter)
            sumStepLength += abs(kind.lastDistance - currentDistance)
        if sumStepLength < 0.001:
            break
        stepCount += 1
        print stepCount
        for kind in ClassModelList:
            s = '***'
            for item in topItemsInDictionary(kind.center.wordsMap,10):
                v = '%f' %kind.center.wordsMap[item]
                s = s + ConvertCN(item) + ':' + v + ', ' 
            print s
        print stepCount
        print '----------'
if __name__ == '__main__':
    initData(DocumentAllModelsPath ('yishuiliunian@gmail.com', 'a') ,10,100)
    predictModelPath = 'predictModel'
    predictFile = open(predictModelPath, 'w')
    pickle.dump(ClassModelList, predictFile)
    predictFile.close()

