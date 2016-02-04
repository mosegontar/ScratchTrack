from catalog_data import CatalogData

class Interface(object):

    def __init__(self):
        self.state = CatalogData() # gets the current state of the database
        self.new_files, self.old_files = self.state.get_status()
