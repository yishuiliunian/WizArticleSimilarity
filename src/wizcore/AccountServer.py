#/user/bin/env python
from HTMLParser import HTMLParser
import pdb
import html2text
import vimpdb
import xmlrpclib
import os
import hashlib
import httplib
import codecs
import zipfile
import datetime
import xmlrpclib
import codecs
import zipfile
import jieba
import pickle
import jieba.posseg as pseg
from xmlrpclib import Server

serverurl = 'http://service.wiz.cn/wizkm/xmlrpc'

def WizServerUrl():
    global serverurl
    if cmp(serverurl, "aaa") != 0:
        return serverurl
    version = 1.0
    debug = 1
    plat = 'ios'
    url = "api.wiz.cn"
    dir = " /?p=wiz&v=%d&c=sync_http&plat=%s&debug=%d" % (version, plat, bool(debug))
    connection = httplib.HTTPConnection(url, 80)
    connection.request('GET', dir)
    serverurl = connection.getresponse().read()
    connection.close()
    return serverurl

class WizDocument():
    def __init__(self, data):
        self.guid = getValueFromNotNilKey('document_guid',data)
        self.version = int(getValueFromNotNilKey('version', data))
        self.title = getValueFromNotNilKey('document_title', data)

class WizXmlServer(Server):
    def addCommonParams(self, postParams):
        postParams['client_type'] = 'python_command'
        postParams['program_type'] = 'normal'
        postParams['api_version'] = 4
def getValueFromNotNilKey(key, dic):
    if dic.has_key(key):
        return dic[key]
    else:
        return None

class WizAccountLoginData:
    def __init__(self, data):
        self.token = getValueFromNotNilKey('token',data)
        self.guid = getValueFromNotNilKey('kb_guid',data)
        self.kapi_url = getValueFromNotNilKey('kapi_url',data)

class WizAccountServer(WizXmlServer):
    def accountLogin(self, userId, password):
        dic = {}
        dic['user_id'] = userId
        dic['password'] = password
        self.addCommonParams(dic)
        logindata = self.accounts.clientLogin(dic)
        return WizAccountLoginData(logindata)

class WizKbServer(WizXmlServer):
    def __init__(self, url ,token, kbguid):
        xmlrpclib.Server.__init__(self, url)
        self.token = token
        self.kbguid = kbguid

    def addCommonParams(self, postParams):
        WizXmlServer.addCommonParams(self, postParams)
        postParams['token'] = self.token
        postParams['kb_guid'] = self.kbguid
    def getDocumentList(self, first, count):
        postParams = {}
        self.addCommonParams(postParams)
        postParams['count']= count
        postParams['version'] = first
        ret = self.document.getSimpleList(postParams)
        if isinstance(ret, list):
            documentlist = []
            for item in ret:
                doc = WizDocument(item)
                documentlist.append(doc)
            return documentlist
        else:
            return []
    def downloadWizObjectData(self, guid, objType, startPos, requestSize):
        postParams = {}
        self.addCommonParams(postParams)
        postParams['obj_guid'] = guid
        postParams['obj_type'] = objType
        postParams['start_pos'] = startPos
        postParams['part_size'] = requestSize 
        return self.data.download(postParams)
    def downloadObject(self, filePath, guid, objType):
        writefile = open(filePath, 'w')
        writefile.seek(0)
        willGetNext = True
        requestSize = 1024*50000
        while willGetNext:
            startPos = writefile.tell()
            ret = self.downloadWizObjectData(guid, objType, startPos, requestSize)
            partData = getValueFromNotNilKey('data', ret)
            isEof = getValueFromNotNilKey('eof', ret)
            obj_size = getValueFromNotNilKey('obj_size', ret)
            if isEof == '1':
                willGetNext = False
            writefile.write(partData.data)
            if int(obj_size) == writefile.tell():
                willGetNext = False
        writefile.close()

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

def wordFrequency(wordsList):
    wordMap = {}
    sumCount = 0
    
    for w in wordsList:
        if '\n' in w:
            w.replace('\n', '')
        if '\t' in w:
            w.replace('\t', '')
        if len(w.strip()) == 0:
            continue 
        sumCount += 1
        try:
            if wordMap.has_key(w):
                count = wordMap[w]
                wordMap[w] = count + 1
            else:
                wordMap[w] = 1
            wordMap[w]
        except KeyError:
            continue
    wrodRatioMap = {}
    if sumCount != 0:
        keys = wordMap.keys()
        for key in keys:
            try:
                count = wordMap[key]
                value = float(count)/sumCount
                wrodRatioMap[key] = float(count)/sumCount
            except KeyError:
                continue
    return subTopItemsIndictionary(wrodRatioMap, 1000)


documentWordsModelPath = './documentModel/'
accountServerUrl = WizServerUrl()
accountServer = WizAccountServer(accountServerUrl)
userId = 'yishuiliunian@gmail.com'
password = '654321'
loginData = accountServer.accountLogin(userId, password)

print 'login succeess'
kb = WizKbServer(loginData.kapi_url, loginData.token, '66e5c3f6-8482-11e1-a525-00237def97cc')
willGetNext = True


versionfilepath = './version.txt'

def getStartCount():
    vf = open(versionfilepath, 'r')
    v = vf.read()
    if v is not None or v != '':
        return int(v)
    else:
        return 0
def setStartCount(ver):
    vf = open(versionfilepath, 'w')
    vstr = '%d' %ver
    vf.write(vstr)
        


IgnoreWordsFeatureList = ['w', 'x', 'u', 'p', 'c' ,'q']

def getWordsWeight(wordFeature):
    if len(wordFeature) < 1:
        return 0
    if wordFeature[0:1] in IgnoreWordsFeatureList:
        return 0
    return 1

def extractWordModel(content):
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
    wrodRatioMap = {}
    if sumCount != 0:
        keys = wordMap.keys()
        for key in keys:
            try:
                count = wordMap[key]
                value = float(count)/sumCount
                wrodRatioMap[key] = float(count)/sumCount
            except KeyError:
                continue
    return subTopItemsIndictionary(wrodRatioMap, 1000)



totalCount = 0
startCount = getStartCount()
while willGetNext:
    print 'parse total count %d' %totalCount 
    documentlist = kb.getDocumentList(startCount + 1, 10)
    totalCount += len(documentlist)
    if len(documentlist) ==0:
        break
    print 'download doument %d' %len(documentlist)
    outPutPath = './sourcefile/'
    maxVer = 0
    for doc in documentlist:
        print 'begin parse document'
        if doc.version > maxVer:
            maxVer = doc.version
            startCount = maxVer
        
        try:
            docguid = doc.guid
            filePath = './data/%s.ziw' %(docguid)
            kb.downloadObject(filePath, docguid , 'document')
            print 'end download'
            zip = zipfile.ZipFile(filePath)
            extracFilePath = './unzip/%s' %(docguid)
            zip.extractall(extracFilePath)
            indexfilepath = extracFilePath + '/index.html'
            indexFile = codecs.open(indexfilepath, 'r', 'utf16')
            contentText = html2text.html2text(indexFile.read())
            indexFile.close()
            ###
            import shutil
            os.remove(filePath)
            shutil.rmtree(extracFilePath)

            ###
            fileName = '%s.txt' %(docguid)
            wordRatio =  extractWordModel(contentText)
            docfilePath = documentWordsModelPath + fileName
            docfile = codecs.open(docfilePath, 'w')
            pickle.dump(wordRatio, docfile)
            print 'end dump'
            setStartCount(doc.version)
        except KeyError:
            pass
        except :
            print '*******error*****'
            pass
    
        print 'edn parse document %s' %doc.title
    setStartCount(maxVer)

