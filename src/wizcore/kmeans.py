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


class Document:
    def __init__(self, title, dataMap):
        self.wordsMap = dataMap
        self.title = title
    def getValueOfWord(self, word):
        if self.wordsMap.has_key(word):
            return self.wordsMap[word]
        return 0
    def distance(self, doc1):
        sum = 0.0
        for word in self.wordsMap.keys():
            w1 = self.wordsMap[word]
            if word in doc1.wordsMap:
                w2 = doc1.wordsMap[word]
                dis = w1 -w2
                sum += dis*dis
            else:
                sum  += w1*w1
        for word in doc1.wordsMap.keys():
            w2 = doc1.wordsMap[word]
            if word not in  self.wordsMap:
                sum += w2 * w2
        return math.sqrt(sum)

class ClassModel:
    def __init__(self, center):
        self.center = center
        self.lastDistance = 10000000000000.0
        self.lastCenter = Document('lastCenter',{})
        self.documentList = []
    def calAvarageCenter(self):
        length = len(self.documentList)
        avarageSumMap = {}
        for document in self.documentList:
            for word in document.wordsMap.keys():
                if avarageSumMap.has_key(word):
                    value =avarageSumMap[word]
                    avarageSumMap[word] = value + document.wordsMap[word]
                else:
                    avarageSumMap[word]=0
        keys = avarageSumMap.keys()
        for word in keys:
            avarageSumMap[word] = avarageSumMap[word] / length
        centerTitle = 'center'
        self.setCenter(Document(centerTitle, avarageSumMap))
    def setCenter(self, center):
        center.wordsMap = maxItemInDictionary(center.wordsMap, 1000)
        self.lastDistance = self.center.distance(self.lastCenter)
        self.lastCenter = self.center
        self.center = center
    def clearDocumentList(self):
        self.documentList = []
    def addDocument(self,document):
        self.documentList.append(document)

import os
import codecs
removeWordsList = ['gif','index',u'和','jpg','1','3','com','4','10', u'了',u'在', u'是' ,'10','2',u'后', u'的', 'place', 'nbsp', 'holder','png','files','http']
def initData(dataFilePath, numberOfKinds, makStepCount):

    global ClassModelList
    wordsMap = {}
    i = 0
    documents = os.listdir(dataFilePath)
    docLength = len(documents)
    randomSeed = len(documents) / numberOfKinds
    totalKindModelCount = 0
    for doc in documents:
        if not doc.endswith('.txt'):
            continue
        filePath = dataFilePath + doc
        sfile = codecs.open(filePath, 'r')
        documentDataMap = pickle.load(sfile)
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
    initData('./documentModel/', 100 ,1)
    predictModelPath = 'predictModel'
    predictFile = open(predictModelPath, 'w')
    pickle.dump(ClassModelList, predictFile)
    predictFile.close()

