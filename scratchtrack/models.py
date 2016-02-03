import os
from peewee import *

db_name = '.'+os.path.basename(os.getcwd()).lower()+'_st.db'
db = SqliteDatabase(db_name) 

class BaseModel(Model):
    """Base Model"""

    class Meta:
        database = db

class File(BaseModel):
    file_name = CharField(unique=True)
    description = TextField()
    date_created = DateTimeField()

class Tag(BaseModel):
    tag_name = CharField(max_length=50, unique=True)

class FileTag(BaseModel):
    file_id = ForeignKeyField(File)
    tag_id = ForeignKeyField(Tag)

