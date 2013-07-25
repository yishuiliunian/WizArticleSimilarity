from sqlalchemy import *

global_table_list = (
    ('meta', (
        Column('kind', String(40)),
        Column('key', String(40)),
        Column('value', Integer),
        )
    ),
)

DBKeyOfTableMeta = 'meta'
KeyOfVersionDocument = 'Document'



class WizDataBase():
    def __init__(self,dbPath):
        self.db = create_engine('sqlite:///' + dbPath)
        self.db.echo = False
        self.metadata = MetaData(self.db)
        self.tableMap = {}
        for (t_name, t_columns) in global_table_list:
            try:
                cur_table = Table(t_name, self.metadata, autoload = True)
            except:
                cur_table = apply(Table, (t_name,self.metadata) + t_columns)
                cur_table.create()
            self.tableMap[t_name] = cur_table
        self.connection = self.db.connect()

    def getTable(self, tName):
        return self.tableMap[tName]
    def getSyncVersion(self, key):
        s = text("""select value from meta where kind=:k1 and key=:k2 """)
        rows = self.connection.execute(s, k1 ='sync', k2 =key)
        if rows is None or rows.rowcount == 0:
            return 0
        
        for row in rows:
            return row['value']
        return -1

    def setSyncVersion(self, key, ver):
        if self.getDocumentVersion() == -1:
            s = text(""" insert into meta (kind, key, value) values(:v1, :v2, :v3)""")
            self.connection.execute(s , v1 = 'sync', v2 = key, v3 = ver)
        else:
            s = text("""update meta set value=:v where kind=:k and key=:key""")
            self.connection.execute(s ,v=ver, k='sync', key = key)
   
        pass  
    def getDocumentVersion(self):
        return self.getSyncVersion(KeyOfVersionDocument)
    def setDocumentVersion(self , ver):
        self.setSyncVersion(KeyOfVersionDocument, ver)
    
 


if __name__ == '__main__':
    db = WizDataBase('a.db')
    db.setDocumentVersion(2)
    print db.getDocumentVersion()




