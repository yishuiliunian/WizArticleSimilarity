class Base(object):
    def __init__(self, key):
        print key
        print "Base created"

class ChildA(Base):
    def __init__(self,key):
        Base.__init__(self,key)

class ChildB(Base):
    def __init__(self, key):
        super(ChildB, self).__init__(key)

print ChildA('a'),ChildB('b')
