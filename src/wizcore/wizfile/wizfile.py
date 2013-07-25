import sys
import os
def ensurePathExist(path):
    if not os.path.exists(path):
        os.mkdir(path)

usr_home = '~'

def AppDataPath():
    global usr_home
    if usr_home == '~':
        usr_home = os.path.expanduser('~')
    return usr_home

def pathJoin(parentPath,subPath):
    if parentPath.endswith('/'):
        return parentPath + subPath
    else:
        return parentPath + '/' + subPath

def AccountHomePath(accountUserId):
    accountPath = pathJoin(AppDataPath(), accountUserId)
    ensurePathExist(accountPath)
    return accountPath
    
def KbHomePath(accountUserId, kbguid):
    accountHome = AccountHomePath(accountUserId)
    kbpath = pathJoin(accountHome, kbguid) 
    ensurePathExist(kbpath)
    return kbpath

def DocumentZiwPath(accountUserId, kbguid, documentguid):
    return pathJoin(KbHomePath(accountUserId, kbguid), documentguid + '.ziw')

def DataBasePath(accountUserId, kbguid):
    return pathJoin(AccountHomePath(accountUserId), kbguid  + '.db')

def DocumentUnZipPath(accountUserId, kbguid, documentguid):
    return pathJoin(KbHomePath(accountUserId, kbguid), documentguid + 'unzip')

def DocumentAllModelsPath(accountUserId, kbguid):
    accountPath = AccountHomePath(accountUserId)
    modelPath = pathJoin(accountPath, 'models')
    ensurePathExist(modelPath)
    return modelPath

def DocumentTFIDFModelsPath(accountUserId, kbguid):
    accountPath = AccountHomePath(accountUserId)
    modelPath = pathJoin(accountPath, 'tfidfmodels')
    ensurePathExist(modelPath)
    return modelPath

def DocumentTFIDFModelFilePath(accountUserId, kbguid):
    modelPath = DocumentTFIDFModelsPath(accountUserId, kbguid)
    return modelPath



def DocumentModelPath(accountUserId, kbguid, documentguid):
    modelPath = DocumentAllModelsPath(accountUserId, kbguid)
    return pathJoin(modelPath, documentguid)

if __name__ == '__main__':
    print DocumentZiwPath('1','1','1')
