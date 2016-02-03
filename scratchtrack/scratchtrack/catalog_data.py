import os
import catalog

class CatalogData(object):

    def __init__(self, directory_files=[]):

        self.cwd = os.getcwd()
        self.db_name = '.'+os.path.basename(self.cwd).lower()+'_st.db'
        self.ignored_files = [os.path.basename(__file__), 'catalog.py', self.db_name]
        self.directory_files = directory_files
        self.catalog_files = catalog.get_entries()
        self.uncataloged_files = []
        self.expired_files = []

    def get_status(self):
        """Retrieves list of files in CWD and list of files in Catalog"""
        
        for item in os.listdir(self.cwd):
            if item not in self.ignored_files and (not item.startswith('.') and '.pyc' not in item):
                self.directory_files.append(item)        
        
        self.uncataloged_files = sorted(list(set(self.directory_files).difference(self.catalog_files)))
        self.expired_files = sorted(list(set(self.catalog_files).difference(self.directory_files)))

        return self.uncataloged_files, self.expired_files