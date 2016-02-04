import os
import datetime
from peewee import *
from models import db, File, Tag, FileTag

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


    files_with_tags = {}

    for file_tag in all_entries:
 
        f = file_tag.file_id
        tag = file_tag.tag_id.tag_name

        files_with_tags.setdefault(f.file_name, []).append(tag)
    
    ordered_list = sorted([f for f in File.select()])

    entries = []
    for f_name in ordered_list:
        f_name.file_name
        f_name.description
        f_name.date_created
        tags = ' | '.join(sorted(files_with_tags.get(f_name.file_name, '')))

        entries.append((f_name.file_name, f_name.description, f_name.date_created, tags))

    return entries

def view_tags(sort_by):

    if sort_by == 'alpha':

        tags_in_use = (Tag
            .select(Tag)
            .join(FileTag)
            .join(File)
            .group_by(Tag))

        tags_in_use_list = sorted([t.tag_name for t in tags_in_use])
        
        return tags_in_use_list

    elif sort_by == 'count':
        
        count = fn.COUNT(FileTag.id)

        tags_with_counts = (Tag
                        .select(Tag, count.alias('entry_count'))
                        .join(FileTag)
                        .join(File)
                        .group_by(Tag)
                        .order_by(count.desc(), Tag.tag_name))

        tags_and_counts = []

        for tag in tags_with_counts:
            tag_name, count =  (tag.tag_name, FileTag.select().where(FileTag.tag_id == tag).count())
            tags_and_counts.append(tag_name+' '+'(%d)' % count)
        
        return tags_and_counts

def get_tags(file_name):

    if File.get(File.file_name == file_name):

        file_tags = (Tag
                      .select()
                      .join(FileTag)
                      .where(FileTag.file_id == File.get(File.file_name == file_name)))
        
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


def search_tags(tags, logic):
    
    if logic == 'and':

        search_with_and = (File
                            .select()
                            .join(FileTag)
                            .join(Tag)
                            .where(
                                (Tag.tag_name << tags))
                            .group_by(File)
                            .having(fn.COUNT(File.id) == len(tags)))

        search_results = search_with_and


    elif logic == 'or':

        search_with_or = (File
                            .select()
                            .join(FileTag)
                            .join(Tag)
                            .where(
                                (Tag.tag_name << tags))
                            .group_by(File))  

        search_results = search_with_or      
    
    else:
        pass

    results = []
    for result in search_results:
        
        result.file_name
        result.description
        result.date_created
        
        tags = get_tags(result.file_name)
        tag_list = ' | '.join(sorted(tags))

        results.append((result.file_name, result.description, result.date_created, tag_list))

    return results        


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
        
        else:
            pass

    except:
        
        print "Whoops. %s not in catalog files." % file_name


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

        print "\n'%s' deleted from catalog\n" % entry

    else:
        pass

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
