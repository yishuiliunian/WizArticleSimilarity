
from WizObject import WizObject

import sys
sys.path.append('../')
from wizglobals import getValueFromNotNilKey
class WizGroup(WizObject):
    def __init__(self, data):
        self.guid = getValueFromNotNilKey('kb_guid', data)
        self.kapiurl = getValueFromNotNilKey('kapi_url', data)

