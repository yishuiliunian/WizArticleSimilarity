from DocumentModel import DocumentModel
from wizglobals import subTopItemsIndictionary

class KindModel:
    def __init__(self, center):
        self.center = center
        self.lastDistance = 10000000000000.0
        self.lastCenter = DocumentModel('lastCenter',{})
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
        self.setCenter(DocumentModel(centerTitle, avarageSumMap))
    def setCenter(self, center):
        center.wordsMap = subTopItemsIndictionary(center.wordsMap, 1000)
        self.lastDistance = self.center.distance(self.lastCenter)
        self.lastCenter = self.center
        self.center = center
    def clearDocumentList(self):
        self.documentList = []
    def addDocument(self,document):
        self.documentList.append(document)


