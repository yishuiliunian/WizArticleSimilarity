import sys
sys.path.append('../')
import pickle
from wizfile import DocumentAllModelsPath
import os
import math
from wizfile import DocumentTFIDFModelsPath

def loadDocumentModelFromFile(filepath):
    sfile = open(filepath, 'r')
    doc = pickle.load(sfile)
    sfile.close()
    return doc

def tfidf(accountUserId, kbguid):
    tfidfPath = DocumentTFIDFModelsPath(accountUserId, kbguid)
    dataFilePath = DocumentAllModelsPath(accountUserId, kbguid)
    documents = os.listdir(dataFilePath)
    docLength = len(documents)
    documentlist = []
    for doc in documents:
        if doc.endswith('Store'):
            continue
        filePath = dataFilePath + '/' +doc
        doc = loadDocumentModelFromFile(filePath)
        documentlist.append(doc)

    totalCountMap = {}
    for doc in documentlist:
        for key in doc.wordsMap.keys():
            if totalCountMap.has_key(key):
                totalCountMap[key] += 1
            else:
                totalCountMap[key] = 1

    doclength = len(documentlist)

    for key in totalCountMap.keys():
        totalCountMap[key] = math.log(doclength/float(totalCountMap[key]))
    for doc in documentlist:
        for key in doc.wordsMap.keys():
            doc.wordsMap[key] = doc.wordsMap[key] * totalCountMap[key]

        outfilepath = tfidfPath + '/' + doc.title
        outfile = open(outfilepath, 'w')
        pickle.dump(doc, outfile)
        outfile.close()

if __name__ == '__main__':

    tfidf('yishuiliunian@gmail.com', 'dddd')



