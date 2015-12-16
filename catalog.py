import os
import datetime

from peewee import *

db_name = os.path.basename(os.getcwd()).lower()+'_st.db'
db = SqliteDatabase(db_name)  


####################################################
#                  TAGGING SCHEMA               

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
                                                 
#####################################################

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def connect_database():
    db.connect()
    db.create_tables([File, Tag, FileTag], safe=True)


def view_all_entries():

    all_entries = (FileTag
              .select(FileTag, File, Tag)
              .join(Tag)
              .switch(FileTag)
              .join(File)
              .order_by(File.file_name))

    last_entry = None

    files_with_tags = {}

    for file_tag in all_entries:
 
        f = file_tag.file_id
        tag = file_tag.tag_id.tag_name
        if f != last_entry:
            last_entry = f

        files_with_tags.setdefault(f.file_name, []).append(tag)
    
    ordered_list = sorted([f for f in File.select()])

    for f_name in ordered_list:
        print 'File: %s' % f_name.file_name
        print 'Description: %s' % f_name.description
        print 'Created on: %s' % f_name.date_created
        print 'Tags: %s' % ' | '.join(sorted(files_with_tags.get(f_name.file_name, '')))
        print


def view_tags(sort_by):

    if sort_by == 'alpha':

        tags_in_use = (Tag
            .select(Tag)
            .join(FileTag)
            .join(File)
            .group_by(Tag))

        tags_in_use_list = sorted([t.tag_name for t in tags_in_use])

        for t in tags_in_use_list:
            print t
        

    elif sort_by == 'count':
        
        count = fn.COUNT(FileTag.id)

        tags_with_counts = (Tag
                        .select(Tag, count.alias('entry_count'))
                        .join(FileTag)
                        .join(File)
                        .group_by(Tag)
                        .order_by(count.desc(), Tag.tag_name))

        for tag in tags_with_counts:
            print "%s (%d)" % (tag.tag_name, FileTag.select().where(FileTag.tag_id == tag).count())
            

    elif File.get(File.file_name == sort_by):

        file_tags = (Tag
                      .select()
                      .join(FileTag)
                      .where(FileTag.file_id == File.get(File.file_name == sort_by)))
        
        tag_list = []
        
        for t in file_tags:
            tag_list.append(t.tag_name)

        return tag_list

    else:
        print "Sorry! Couldn't understand request!"

def get_entries():
    """gets all file names currently in catalog"""

    catalog_files = []

    if File.select():
        for item in File.select():
            catalog_files.append(item.file_name)
    else:
        return catalog_files

    return catalog_files


def search_tags(logic, tags):
    clear_screen()
    if logic == 'and':

        search_with_and = (File
                            .select()
                            .join(FileTag)
                            .join(Tag)
                            .where(
                                (Tag.tag_name << tags))
                            .group_by(File)
                            .having(fn.COUNT(File.id) == len(tags)))

        print

        if len(search_with_and) > 0:
           
            print "SEARCH RESULTS:\n"
            print "Searching for: %s" % (' AND '.join(tags))

        print

        for result in search_with_and:
            
            print "File: %s" % result.file_name
            print "Description: %s" % result.description
            print "Date Created: %s" % result.date_created
            
            tags = view_tags(result.file_name)
            print "Tags: %s" % (' | '.join(sorted(tags)))
            print


    elif logic == 'or':

        search_with_or = (File
                            .select()
                            .join(FileTag)
                            .join(Tag)
                            .where(
                                (Tag.tag_name << tags))
                            .group_by(File))
        print

        if len(search_with_or) > 0:

            print "SEARCH RESULTS:\n"
            print "Searching for: %s" % (' OR '.join(tags))
        
        print

        for result in search_with_or:
            
            print "File: %s" % result.file_name
            print "Description: %s" % result.description
            print "Date Created: %s" % result.date_created
            
            tags = view_tags(result.file_name)
            print "Tags: %s" % (' | '.join(sorted(tags)))
            print


    else:

        print "We're afraid there was a problem with your query :( "


def add_tag(tag):

    tag = tag.strip()

    new_tag = False

    try:
        current_tag = Tag(tag_name=tag)
        current_tag.save()
        new_tag = True

    except IntegrityError:
        current_tag = Tag.get(Tag.tag_name == tag)

    return current_tag, new_tag

def add_file(file_name, description=None):

    file_name = file_name.strip()

    try:
        date_created = datetime.datetime.fromtimestamp(os.path.getctime(file_name)).strftime('%Y-%m-%d %H:%M:%S')
        current_file = File(file_name=file_name, 
                            description=description, 
                            date_created=date_created)


        current_file.save()
        print "\n'%s' added!\n" % file_name

    except IntegrityError:
        current_file = File.get(File.file_name == file_name)

    return current_file

def tag_a_file(file_name, tag, new_tag):

    if not new_tag:
        files_with_tag = (File
                            .select()
                            .join(FileTag)
                            .join(Tag)
                            .where(FileTag.tag_id == Tag.get(Tag.tag_name == tag.tag_name)))

        for f in files_with_tag:
            if file_name.file_name == f.file_name:
                return

    try:
        ft = FileTag(file_id=file_name, tag_id=tag)
        ft.save()
    except IntegrityError:
        return

    print "'%s' added to %s tags!" % (tag.tag_name, file_name.file_name)


def edit_description(file_name):

    try:

        f = File.get(File.file_name == file_name.strip())
  
        print "\nCurrent %s description: '%s'\n" % (f.file_name, f.description)

        choice = raw_input("Replace current description? Y/N: ")

        if choice.lower() == 'y':
            new_description = raw_input("\nEnter new description for '%s': " % f.file_name)
            
            f.description = new_description

            f.save()
            
            print "\nNew Description Saved to %s!" % f.file_name
            print
        
        else:
            print "\Skipped! You didn't say (Y)ES \n"

    
    except:
        
        print "Whoops. %s not in catalog files. Enter -v to see list of all catalog files" % file_name


def delete_entry(kind, entry, from_file=None):
    
    if kind == 'files':

        to_delete = File.get(File.file_name == entry)

        to_delete.delete_instance()

        print "\n%s deleted from catalog!\n" % entry

    elif kind == 'tag' and from_file:

        try:
            existing_file = File.get(File.file_name == from_file)

            if existing_file:
                try:
                    association = FileTag.get(FileTag.file_id == existing_file, FileTag.tag_id == Tag.get(Tag.tag_name == entry))
                    
                    association.delete_instance()

                    print "Deleted '%s' from '%s'" % (entry, from_file)

                except:

                    print "'%s' no longer tagged to %s" % (entry, from_file)

        except:
            print "'%s' not in catalog" % from_file

    elif kind == 'tag':

        tag_item = Tag.get(Tag.tag_name == entry)

        tag_item.delete_instance()

        print "'%s' deleted from catalog" % entry

        all_associations = FileTag.select().join(Tag).where(Tag.tag_name == entry)
        
        for i in all_associations:
            print i

    else:
        print "Delete Entry Error: Sorry! There's a problem somewhere"

def clean_db():

    all_tags = Tag.select()
    
    all_tags_list = []

    for tag in all_tags:
        all_tags_list.append(tag)

   
    tags_in_use = (Tag
                .select(Tag)
                .join(FileTag)
                .join(File)
                .group_by(Tag))

    tags_in_use_list = []

    for tag in tags_in_use:
        tags_in_use_list.append(tag)

    for tag in all_tags_list:
        if tag not in tags_in_use_list:
            tag.delete_instance()
