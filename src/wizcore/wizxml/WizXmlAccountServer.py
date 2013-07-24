from WizXmlServer import WizXmlServer
import sys
sys.path.append('../')
from wizurl import WizServerUrl
from wizglobals import getValueFromNotNilKey
from wizmodel import WizGroup

class WizAccountLoginData:
    def __init__(self, data):
        self.token = getValueFromNotNilKey('token',data)
        self.guid = getValueFromNotNilKey('kb_guid',data)
        self.kapi_url = getValueFromNotNilKey('kapi_url',data)
        self.loginData = None 

class WizXmlAccountServer(WizXmlServer):
    def accountLogin(self, userId, password):
        dic = {}
        dic['user_id'] = userId
        dic['password'] = password
        self.addCommonParams(dic)
        logindata = self.accounts.clientLogin(dic)
        self.loginData = WizAccountLoginData(logindata)
        return self.loginData     
    def getAllGroups(self):
        dic = {'token':self.loginData.token}
        self.addCommonParams(dic)
        groups = self.accounts.getGroupKbList(dic)
        grouplist = []
        for dic in groups:
            g = WizGroup(dic)
            grouplist.append(g)
        return grouplist


if __name__ == '__main__':

    s = WizXmlAccountServer(WizServerUrl())
    s.accountLogin('yishuiliunian@gmail.com', '654321')
    print s.getAllGroups()

    pass
