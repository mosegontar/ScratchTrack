import catalog
from catalog_data import CatalogData

class Editor(object):

    def __init__(self):

        self.state = CatalogData()
        self.new_files, self.old_files = self.state.get_status()

    def add_files(self, args):
        """Add an uncataloged file from CWD to catalog"""

        file_name = args.filename.strip()

        if file_name not in self.new_files:
            print "'%s' either already in catalog or not in the CWD\n" % file_name
            return
            

        description = raw_input("Enter file description: ")

        current_file = catalog.add_file(file_name, description)

    def add_tag(self, args):
        """Add tag(s) to a file"""

        file_name = args.filename.strip()
        tag_list = [tag.strip() for tag in args.tags]

        try:
            current_file = catalog.File.get(catalog.File.file_name == file_name)
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

    def edit_entry(self, args):
        """Edit file description"""

        catalog.edit_description(args.filename)

    def clean_catalog(self, args):
        """
        Removes all expired entries from catalog

        If optional argument [-t] used, removes specified tags from entire catalog
        """

        if not self.old_files:
            
            print "There are no expired entries in the catalog"

        else:
            choice = raw_input("Delete all expired entries in the catalog? Press 'Y' to continue.")

            if choice.lower() == 'y':

                for file_name in self.old_files:

                    # These are the tags currently associated with the to-be-deleted file name
                    file_name_tags = catalog.get_tags(file_name)
                    
                    # Deletes file-tag relationships first. Needed to ensure that database remains clean
                    # and that when viewing tags sorted by count, the numbers are accurate.
                    for tag_name in file_name_tags:
                        catalog.delete_entry('tag', tag_name.lower().strip(), file_name)
                    
                    # Now delete the officially delete the entry from the database
                    catalog.delete_entry('files', file_name)
            else:
                pass


        # delete specified tags from entire catalog
        if args.tags:

            for tag in args.tags:
                catalog.delete_entry('tag', tag.strip())   
        else:
            pass
  
    def delete_entry(self, args):
        """
        Removes specified file from catalog

        If optional argument [-t] used, removes tags from their association with specified file (file remains in catalog)
        """

        file_name = args.file.strip()

        if not args.tags:
            choice =  raw_input("Remove '%s' from Scratch Track catalog entirely?\nPress 'Y' to continue: " % args.file.strip())
            
            if choice.lower() == 'y':

                # These are the tags currently associated with the to-be-deleted file name
                file_name_tags = catalog.get_tags(file_name)
                
                # Deletes file-tag relationships first. Needed to ensure that database remains clean
                # and that when viewing tags sorted by count, the numbers are accurate.
                for tag_name in file_name_tags:
                    catalog.delete_entry('tag', tag_name.lower().strip(), file_name)
                
                # Now delete the officially delete the entry from the database
                catalog.delete_entry('files',file_name)                
        else:

            # delete specified tag(s) association from specified file  
            for tag in args.tags:
                
                catalog.delete_entry('tag', tag.strip(), file_name)


    def merge_tags(self, args):
        """Takes tags from a source file and adds them to a destination file"""

        # check if source file actually exists
        try: 
            old_exists = catalog.File.get(catalog.File.file_name == args.source)
        except:
            print "Sorry! '%s' isn't  in the catalog" % args.source
            return

        # check if destination file actually exists
        try:    
            new_exists = catalog.File.get(catalog.File.file_name == args.dest)
        except:
            print "Sorry! '%s' isn't  in the catalog" % args.dest
            return
    
        source_file_tags = set(catalog.get_tags(args.source))
        dest_file_tags = set(catalog.get_tags(args.dest))

        union_of_source_dest_tags = source_file_tags.union(dest_file_tags)

        current_file = catalog.File.get(catalog.File.file_name == args.dest)

        # take tags unique to source file and give them to destination file 
        for tag in union_of_source_dest_tags:
            tag = catalog.Tag.get(catalog.Tag.tag_name == tag)
            catalog.tag_a_file(current_file, tag, False)
        