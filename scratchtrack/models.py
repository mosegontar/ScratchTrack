import os
from peewee import *

db_name = '.'+os.path.basename(os.getcwd()).lower()+'_st.db'
db = SqliteDatabase(db_name)


class BaseModel(Model):
    """Base Model"""

    class Meta:
        database = db


class File(BaseModel):
    """
    File model.
    Every file has 3 associated fields:
    file name, description, and creation date
    """

    file_name = CharField(unique=True)
    description = TextField()
    date_created = DateTimeField()


class Tag(BaseModel):
    """Tag model. Every tag has 3=1 associated field (tag name)"""

    tag_name = CharField(max_length=50, unique=True)


class FileTag(BaseModel):
    """Enables many-to-many matching between files and tags"""

    file_id = ForeignKeyField(File)
    tag_id = ForeignKeyField(Tag)
