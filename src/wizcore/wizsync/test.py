
import sys
sys.path.append('../')

from wizxml import WizXmlAccountServer
from wizxml import *
from wizurl import WizServerUrl
from WizSyncKb import WizSyncKb
import thread



accountS = WizXmlAccountServer(WizServerUrl())
user = 'yishuiliunian@gmail.com'
password = '654321'

loginData = accountS.accountLogin(user, password)
groups =  accountS.getAllGroups()

import threading

con = threading.Condition()

def syncData(accountUserId , kbguid, url , token):
    synckb = WizSyncKb(accountUserId, kbguid, url, token)
    synckb.downloadAllDocuments()
    

thread.start_new_thread(syncData, (user, loginData.guid, loginData.kapi_url, loginData.token))

for g in groups:
    thread.start_new_thread(syncData, (user, g.guid, g.kapiurl, loginData.token))
import time

time.sleep(10000000)




