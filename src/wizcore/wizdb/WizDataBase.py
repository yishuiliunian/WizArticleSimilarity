from sqlalchemy import *

global_table_list = (
    ('meta', (
        Column('kind', String(40)),
        Column('key', String(40)),
        Column('value', Integer),
        )
    ),
)

KeyOfVersionDocument = 'Document'

class WizDataBase():
    def __init__(self,dbPath):
        self.db = create_engine('sqlite:///' + dbPath)
        self.db.echo = False
        self.metadata = MetaData(self.db)
        for (t_name, t_columns) in global_table_list:
            try:
                cur_table = Table(t_name, self.metadata, autoload = True)
            except:
                cur_table = apply(Table, (t_name,self.metadata) + t_columns)
                cur_table.create()

    def getSyncVersion(self, key):
        return 1;
    def setSyncVersion(self, key, ver):
        pass

    def getDocumentVersion(self):
        return self.getSyncVersion(KeyOfVersionDocument)
    def setDocumentVersion(self , ver):
        self.setSyncVersion(self,KeyOfVersionDocument, ver)
    
 


if __name__ == '__main__':
    db = WizDataBase('a.db')





