
import sys
sys.path.append('../')

from wizxml import WizXmlAccountServer
from wizxml import *
from wizurl import WizServerUrl
from WizSyncKb import WizSyncKb



accountS = WizXmlAccountServer(WizServerUrl())
user = 'yishuiliunian@gmail.com'
password = '654321'

loginData = accountS.accountLogin(user, password)
groups =  accountS.getAllGroups()

synckb = WizSyncKb(user, loginData.guid, loginData.kapi_url, loginData.token)
synckb.downloadAllDocuments()
for g in groups:
    synckb = WizSyncKb(user, g.guid, g.kapiurl, loginData.token)
    synckb.downloadAllDocuments()



