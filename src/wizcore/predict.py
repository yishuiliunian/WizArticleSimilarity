import pickle
import os
from kmeans import Document, ClassModel

modelfilepath = 'predictModel'
modelfile = open(modelfilepath, 'r')
modellist = pickle.load(modelfile)
modelfile.close()


dataFilePath = './documentModel/'
predictFileName = '23e8ed27-0a8e-4c48-aef3-642f1c5171cb'

def loadDocument(name):
    docs = os.listdir(dataFilePath)
    name = name + '.txt'
    for doc in docs:
        if name == doc:
            filePath = dataFilePath + doc
            dataMaps = pickle.load(open(filePath, 'r'))
            return Document(doc, dataMaps)
    return None

predictDoc = loadDocument(predictFileName)

maxModel = None

maxLength = -99999999

for m in modellist:
    distance = m.center.distance(predictDoc)
    if distance > maxLength:
        maxLength = distance
        maxModel = m

for doc in m.documentList:
    print doc.title



