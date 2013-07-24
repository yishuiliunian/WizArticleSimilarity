from WizObject import WizObject
import sys
sys.path.append('../')
from wizglobals import getValueFromNotNilKey
from wizglobals import getIntValueFromNotNilKey

class WizDocument(WizObject):
    def __init__(self, data): 

        self.guid = getValueFromNotNilKey('document_guid',data)
        self.version = getIntValueFromNotNilKey('version', data)
        self.title = getValueFromNotNilKey('document_title', data)

if __name__ == '__main__':
    m = {'a':1}
    print getIntValueFromNotNilKey('a', m)
    a = WizObject()
    print a.title
    doc = WizDocument({})
    print doc.title
