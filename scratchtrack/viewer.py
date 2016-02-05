import catalog
from interface import Interface


class Viewer(Interface):
    """
    This class retrieves and displays all
    'viewable' data from the working database
    """

    def status(self, args):
        """
        Displays new files (uncataloged files),
        and expired files (files no longer in CWD)
        """

        if self.new_files:

            print 'New Files Found!\n'
            for file_name in self.new_files:
                print file_name
        else:
            pass

        if self.old_files:

            print 'Old Files Found:\n'
            for index, file_name in enumerate(self.old_files):
                print '[%d]' % (index+1), file_name
        else:
            pass

    def view_full_catalog(self, args):
        """
        Shows every file in catalog, along with each file's
        description, tags, and date created
        """

        entries = catalog.view_all_entries()

        for entry in entries:
            print 'File: %s' % entry[0]
            print 'Description: %s' % entry[1]
            print 'Created on: %s' % entry[2]
            print 'Tags: %s' % entry[3]
            print

    def view_all_tags(self, args):
        """Shows a list of tags, sorted either by count or alphabetically"""

        if args.alpha is False:
            sort_by = 'count'
        else:
            sort_by = 'alpha'

        tags = catalog.view_tags(sort_by)

        for tag in tags:

            print tag

    def search_tags(self, args):
        """
        Searches for files based on tag queries.

        Default uses the AND logical operator
        but optional argument [-o] uses OR
        """

        if args.o:
            logic = 'or'
        else:
            logic = 'and'

        search_term_list = [term.strip() for term in args.tags]

        results = catalog.search_tags(search_term_list, logic.lower())

        for result in results:
            print 'File: %s' % result[0]
            print 'Description: %s' % result[1]
            print 'Created on: %s' % result[2]
            print 'Tags: %s' % result[3]
            print
