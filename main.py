#!/usr/bin/env python

import os
import sys
from collections import OrderedDict

import catalog
from peewee import *

cwd = os.getcwd()
db_name = os.path.basename(cwd).lower()+'_st.db'


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_status():
    """Returns two lists: new files in CWD and old files in catalog"""
    
    ignore_files = [os.path.basename(__file__), 'scratch_track_catalog.py', db_name]
        
    # gets items in current working directory
    directory_files = []

    for item in os.listdir(cwd):

        if item not in ignore_files and (not item.startswith('.') and '.pyc' not in item):

            directory_files.append(item)

    # gets all file names in catalog        
    catalog_files = catalog.get_entries()    

    # set operations used to sort files into new files (uncataloged) and old files (not in cwd)
    uncataloged_files = sorted(list(set(directory_files).difference(catalog_files)))
    files_not_in_cwd = sorted(list(set(catalog_files).difference(directory_files)))
    
    return uncataloged_files, files_not_in_cwd


def display_status(start=False):
    """Displays new files in CWD if found and old files in catalog if found"""
    
    clear_screen()
    
    if start:
        splash()

    new_files, old_files = get_status()

    if new_files:

        print "NEW FILES FOUND:"
        print 'To add these files to catalog, enter -f\n'
        print '    File Name:'
        print '    --------- '
        
        for i, f in enumerate(new_files):   
            print '[%d]' % (i+1), f

        print
    
    else:
        pass

    if old_files:

        print "FILES IN CATALOG FOUND THAT ARE NOT IN CURRENT WORKING DIRECTORY:"
        print '"-d > **f" to delete and remove old files from catalog.\n'
        
        for i, f in enumerate(old_files):
            print '[%d]' % (i+1), f

        print
    
    else:
        pass

    if not start and not (new_files or old_files):
        print "\nEverything's up to date!\n"

def view_catalog(sort_by=None):
    """View Catalog Entries

    USAGE:
    -v         : view all entries in catalog
    -v > alpha : view tags, sorted alphabetically
    -v > count : view tags, sorted by popularity
    """

    clear_screen()
    
    print "VIEWING CATALOG"
    print "---------------"

    if not sort_by:

        print "Enter 'alpha' to view tags alphabetically"
        print "Enter 'count' to view tags by count"
        print
        print "OR just press ENTER to view all entries in the catalog"

        choice = raw_input("> ")
        
        if choice.strip() == '':
        
            print
            catalog.view_all_entries()
            return
        
        else:
            sort_by = choice.strip()

    if sort_by.lower() == 'alpha':

        print '\nTAGS - Sorted alphabetically\n'
        catalog.view_tags(sort_by)
        print

    elif sort_by.lower() == 'count':
        
        print '\nTAGS - Sorted by count\n'
        catalog.view_tags(sort_by)
        print

    else:

        print "\nSorry. Couldn't understand command. See usage:\n"
        print view_catalog.__doc__


def search(logic=None, search_term=None):
    """SEARCH TAGS

    USAGE:
    -s                       : launches search menu
    -s > and > tag1, tag2... : search for tag(s) using OR logic
    -s > or > tag1, tag2...  : search for tag(s) using AND logic
    """

    if not logic and not search_term:
        
        print "Enter search type ('and' / 'or'): " 
        
        logic = raw_input("> ").lower().strip()

        print "Enter search term(s): "

        search_term = raw_input("> ").strip()

    elif not logic:

        print 'Sorry! See search usage:'
        print search.__doc__
        return

    search_term_list = [term.strip() for term in search_term.split(',')]

    catalog.search_tags(logic.lower(), search_term_list)


def add_tag(file_name=None, tags=None):
    """ADD TAG

    USAGE:
    -t                             : launches add_tag menu
    -t > filename > tag1, tag2,... : adds tags to file entry
    """

    if tags:
        tag_list = [t.strip() for t in tags.split(',')]



    # menu
    if not (file_name or tags):

        print "Enter -v to view catalog\n"
        
        to_file = raw_input("Enter file name to tag\n> ").strip()

        # check to see if file exists
        try:
            does_to_file_exist = catalog.File.get(catalog.File.file_name == to_file)
        except:
            print "%s isn't a file in the catalog!\nEnter -v to see list of files in catalog\n" % to_file
            return
    
        tag_list = [tag.strip() for tag in raw_input("Enter tags to add to '%s': "  % to_file).split(',')]
        
        current_file = catalog.File.get(catalog.File.file_name == to_file)
        
        for tag in tag_list:
            
            if tag.strip() == '':
                pass

            else:
                current_tag, new_tag = catalog.add_tag(tag)
                catalog.tag_a_file(current_file, current_tag, new_tag)
                print



    # menu skipped
    elif file_name and tags:

        file_name = file_name.strip()
        
        # check to see if file exists
        try:
            current_file = catalog.File.get(catalog.File.file_name == file_name)
            print
        except:
            print "\nSorry! %s not in catalog! Enter -v to see list of files in catalog\n" % file_name
            return

            
        for tag in tag_list:

            if tag.strip() == '':
                pass

            else:
                current_tag, new_tag = catalog.add_tag(tag)
                catalog.tag_a_file(current_file, current_tag, new_tag)
                print


def add_file(files=None):
    """Adds file name to database\n"""

    new_files, old_files = get_status()

    # if files are not specified, adds all files that are in CWD and not in catalog
    if not files:

        if not new_files:

            clear_screen()
            print "No new files found in CWD"
            return

        else:
            choice = raw_input("\nAdd ALL new files? [Y/N]\n> ")

            if choice.lower() == 'y':
                
                files = new_files
    else:
        files = files.split(',')



    # add all files in 'files' to the catalog
    for file_name in files:

        if file_name not in new_files:
            print
            print "%s either already in catalog or not in the CWD\n" % file_name
            return

        print
        print '%s:' % file_name
        print '-' *len(file_name)
    
        description = raw_input("Enter file description: ")
        tags = [tag.strip() for tag in raw_input("Enter tags, separated by commas: ").split(',')]
        
        current_file = catalog.add_file(file_name, description)
    
        for tag in tags:

            if tag.strip() == '':
                pass
                
            else:
                current_tag, new_tag = catalog.add_tag(tag)
                catalog.tag_a_file(current_file, current_tag, new_tag)
        print
        
def edit_entry(files=None):
    """Edit Entry Description

    USAGE:
    -e 
    -e > file_name1, file_name2,... : edit description of file(s)
    """

    if not files:

        f_name =  raw_input("Enter file name you wish edit: ")

        catalog.edit_description(f_name)

    else: # file names were already entered
        
        files = files.split(',')
        for f in files:

            catalog.edit_description(f)


def merge_tags():
    """Merge Tags

    USAGE:
    -m : Launch  Merge Entry Menu. 

    (Note: Merge does not take any additional arguments.)
    """

    print
    old_file = raw_input("Enter the name of the origin file: ").strip()

    # check if 'old_file' actually exists
    try: 
        o_exists = catalog.File.get(catalog.File.file_name == old_file)
    
    except:
        print "\nSorry! %s isn't  in the catalog\nEnter -v to see list of files in catalog" % old_file
        return
    
    
    new_file = raw_input("Enter the name of the destination file: ").strip()
    print

    # check if 'new_file' actually exists
    try:    
        n_exists = catalog.File.get(catalog.File.file_name == new_file)
    
    except:
        print "\n%s not in catalog! If file in CWD, enter -f to add file to CWD" % new_file
        return
    

    old_file_tags = set(catalog.view_tags(old_file))
    new_file_tags = set(catalog.view_tags(new_file))

    union_of_old_new_tags = old_file_tags.union(new_file_tags)

    current_file = catalog.File.get(catalog.File.file_name == new_file)

    # take tags unique to old_file and give them to new_file 
    for tag in union_of_old_new_tags:
        tag = catalog.Tag.get(catalog.Tag.tag_name == tag)
        catalog.tag_a_file(current_file, tag, False)
    
    print

    # ask user if they'd like to remove the old_file from the catalog entirely
    choice = raw_input("Delete %s? Y/N: " % old_file)
    print

    if choice.lower() == 'y':
        delete_entry('*f', old_file)

    print

def delete_entry(target, items=None):
    """Delete Entry

    USAGE:
    -d > file_name > tag(s). : delete tag(s) from file                           
    -d > *f > file_name(s)   : delete file from catalog
    -d > *t > tag(s)         : delete tag from catalog entirely (deletes it from all associations)
    -d > **f                 : delete files in catalog that are not in CWD
    """

    if items:

        item_list = items.split(',')

    # delete specified tag(s) association from specified file
    if '*' not in target and (target and items):

        from_file = target
        
        for tag in item_list:
            
            catalog.delete_entry('tag', tag.strip(), from_file)
            
    
    else: 

        # delete all old files
        if target == '**f':
            new_files, old_files = get_status()
            
            if not old_files:
                
                print "There are no old files in the catalog."

            else:
                choice = raw_input("Delete All Old Files From Catalog?\nY/N: ") 
        
                if choice.lower() == 'y':
                
                    for f_name in old_files: 

                        # these are the tags currently associated with the to-be-deleted file name
                        f_name_tags = catalog.view_tags(f_name)
                        
                        # deletes file-tag relationships first. Needed to ensure that database remains clean
                        # and that when viewing tags sorted by count, the numbers are accurate.
                        for tag_name in f_name_tags:
                            catalog.delete_entry('tag', tag_name.lower().strip(), f_name)
                        
                        # Now delete the officially delete the entry from the database
                        catalog.delete_entry('files', f_name)



        # delete specified file entries from catalog
        elif target == '*f' and items:

            for item in item_list:

                # these are the tags currently associated with the to-be-deleted file name
                f_name_tags = catalog.view_tags(item)
            
                # deletes file-tag relationships first. Needed to ensure that database remains clean
                # and that when viewing tags sorted by count, the numbers are accurate.
                for tag_name in f_name_tags:
                    catalog.delete_entry('tag', tag_name.strip(), item)

            print
            
            # now delete all specified files from catalog
            for file_found in item_list:
             
                catalog.delete_entry('files', file_found.strip())



        # delete specified tag from entire catalog
        elif target == '*t' and items:

            for item in item_list:
                catalog.delete_entry('tag', item.strip())
        else:

            print "Sorry! Couldn't understand request. Enter -h for help."


def parse_command(command):

    if len(command.split()) == 1 or '-h' in command.lower():
        
        if command not in menu.keys():
            clear_screen()
            print "\n'%s' is not a valid command. Enter -h for help.\n" % command
            
        else:
            menu[command]()
        return

    try:
        directive, destination, items = [c.strip() for c in command.split('>')]

        if directive not in menu.keys():
            clear_screen()
            print "\n'%s' is not a valid command. Enter -h for help.\n" % directive

        else:
            menu[directive](destination, items)

    except ValueError:

        try:
            directive, items = [c.strip() for c in command.split(">")]

            if directive not in menu.keys():
                clear_screen()
                print "\n'%s' is not a valid command. Enter -h for help.\n" % directive
            
            else:
                menu[directive](items)
                return
        
        except:
            clear_screen()
            print "\nDidn't understand entry! Enter -h for help" 


def help_menu():
    """Help Menu\n"""
    
    clear_screen()
    
    print 'HELP MENU:\n'
    
    for key, value in menu.items():
        print "%s: %s" % (key, value.__doc__)
        

def main_menu():

    clear_screen()

    display_status(True)
 
    
    
    quit = False

    while not quit:
        
        print 'SCRATCH TRACK Menu. CWD: %s' % (os.getcwd())
        print '------------------------------------------------------------------------------'
        print " -v = view entries | -t = add tag | -s = search | -q = quit | -h = help/usage"
        print '------------------------------------------------------------------------------'

        user_input = raw_input("> ")
        
        if user_input.lower() == '-q':
            quit = True
        else:
            parse_command(user_input)


menu = OrderedDict([
  ('-f', add_file),
  ('-d', delete_entry),
  ('-t', add_tag),
  ('-e', edit_entry),
  ('-m', merge_tags),
  ('-v', view_catalog),
  ('-s', search),
  ('-h', help_menu),
  ('-u', display_status)])



def splash():
        print """
*************
*           * 
*  Scratch  *
*   Track   *
*           *
*************
"""

if __name__ == '__main__':
    
   catalog.connect_database()
   catalog.clean_db()
   main_menu()


