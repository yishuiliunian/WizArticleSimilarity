from DocumentWordsModel import ExtractDocumentRatioModel

class DocumentModel:
    def __init__(self, title, wordsCountMap):
        self.title = title
        self.wordsMap= wordsCountMap
    
    def loadCountMapFromFile(self, filePath):
        self.wordsMap= ExtractDocumentRatioModel(filePath)

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



