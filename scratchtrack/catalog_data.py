import os
import catalog
from models import db_name
from scratchtrack_ignore import ignored

class CatalogData(object):

    def __init__(self, directory_files=[]):
        """Provides data on the current state of the database"""

        self.cwd = os.getcwd()
        self.db_name = db_name
        self.ignored_files = ignored
        self.directory_files = directory_files
        self.catalog_files = catalog.get_entries()
        self.uncataloged_files = []
        self.expired_files = []

    def get_status(self):
        """Retrieves list of files in CWD and list of files in Catalog"""
        
        for item in os.listdir(self.cwd):
            if item not in self.ignored_files and (not item.startswith('.') and '.pyc' not in item):
                self.directory_files.append(item)        
        
        # Uses set operations to separate out those files that are not in both the CWD and the catalog 
        # into 'uncataloged' and 'expired' lists.
        self.uncataloged_files = sorted(list(set(self.directory_files).difference(self.catalog_files)))
        self.expired_files = sorted(list(set(self.catalog_files).difference(self.directory_files)))

        return self.uncataloged_files, self.expired_files
