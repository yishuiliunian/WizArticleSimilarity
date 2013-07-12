from peewee import *

db = SqliteDatabase('data.db')

class WizMeta(Model):
    kind = CharField()
    value = CahrField()
    class Meta:
        databaser = db

WizMeta.create_table()

def WizMetaSyncVersiondd(kind):
    
