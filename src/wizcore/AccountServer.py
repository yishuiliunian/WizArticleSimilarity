#/user/bin/env python

import pdb
import vimpdb
import xmlrpclib
import os
import hashlib
import httplib
import codecs
import zipfile
import datetime
import xmlrpclib
import zipfile
from xmlrpclib import Server

class WizDocument():
    def __init__(self, data):
        self.guid = getValueFromNotNilKey('document_guid',data)

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
        postParams['start_post'] = startPos
        postParams['part_size'] = requestSize 
        return self.data.download(postParams)
    def downloadObject(self, filePath, guid, objType):
        writefile = open(filePath, 'w')
        writefile.seek(0)
        willGetNext = True
        requestSize = 1024*50000
        while willGetNext:
            startPos = writefile.tell()
            pdb.set_trace()
            ret = self.downloadWizObjectData(guid, objType, startPos, requestSize)
            partData = getValueFromNotNilKey('data', ret)
            isEof = getValueFromNotNilKey('eof', ret)
            print isEof
            obj_size = getValueFromNotNilKey('obj_size', ret)
            if isEof == '1':
                willGetNext = False
            writefile.write(partData.data)
            if int(obj_size) == writefile.tell():
                willGetNext = False
        writefile.close()


accountServer = WizAccountServer('http://service.wiz.cn/wizkm/xmlrpc')
loginData = accountServer.accountLogin('yishuiliunian@gmail.com', '654321')

kb = WizKbServer(loginData.kapi_url, loginData.token, loginData.guid)
documentlist = kb.getDocumentList(0, 1000)
for doc in documentlist:
    filePath = './data/%s.ziw' %(doc.guid)
    kb.downloadObject(filePath, doc.guid, 'document')
    zip = zipfile.ZipFile(filePath)
    extracFilePath = './unzip/%s' %(doc.guid)
    zip.extractall(extracFilePath)
