import sys
sys.path.append('../')
from wizdb import WizDataBase
from wizfile import DataBasePath
from wizxml import WizXmlAccountServer
from wizxml import WizXmlKbServer
from wizfile import DocumentZiwPath
from wizsamemodel import DocumentModel
import pickle

class WizSyncKb():
    def __init__(self, accountUserId ,kbguid, kburl, token):
       self.kbserver = WizXmlKbServer(kburl, token, kbguid)
       self.accountUserId = accountUserId
       self.kbguid = kbguid
       self.kbDataBase = WizDataBase(DataBasePath(accountUserId, kbguid))
    def downloadAllDocuments(self):
        version = self.kbDataBase.getDocumentVersion()
        willGetNext = True
        while willGetNext:
            documentlist = self.kbserver.getDocumentList(version + 1, 10)
            maxVer = 0
            if len(documentlist) == 0:
                break
            for doc in documentlist:
                print doc.guid
                if doc.version > maxVer:
                    maxVer = doc.version
                docguid = doc.guid
                filePath = DocumentZiwPath(self.accountUserId, self.kbguid, docguid)
                self.kbserver.downloadObject(filePath, docguid, 'document')
                from wizfile import DocumentUnZipPath
                import zipfile

                import shutil
                try:
                    azip = zipfile.ZipFile(filePath)
                    extractPath = DocumentUnZipPath(self.accountUserId, self.kbguid, docguid)
                    azip.extractall(extractPath)
                    indexfilepath = extractPath + '/index.html'
                    model = DocumentModel(docguid, {})
                    model.loadCountMapFromFile(indexfilepath)
                    azip.close()
                    shutil.rmtree(extractPath)
                    shutil.os.remove(filePath)
                except:
                    import os
                    if os.path.exists(extractPath):
                        shutil.rmtree(extractPath)
                    if os.path.exists(filePath):
                        shutil.os.remove(filePath)
                     
                
                from wizfile import DocumentModelPath
                try:
                    modelPath = DocumentModelPath(self.accountUserId, self.kbguid, docguid)
                except:
                    print '******error****** %s' %docguid
                    continue
                modelfile = open(modelPath, 'w')
                pickle.dump(model, modelfile)
                modelfile.close()
            
            self.kbDataBase.setDocumentVersion(maxVer)
            if maxVer <= version:
                break
            version = maxVer

