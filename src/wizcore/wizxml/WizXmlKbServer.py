import sys
sys.path.append('../')

from wizglobals import  getValueFromNotNilKey
from WizXmlServer import WizXmlServer
import xmlrpclib
from wizmodel import WizDocument


class WizXmlKbServer(WizXmlServer):
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

