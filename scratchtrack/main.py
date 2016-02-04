#!/usr/bin/env python

import sys
import os
import argparse

from peewee import *
import catalog

from catalog_data import CatalogData
from viewer import Viewer
from editor import Editor

     

class Connection(object):

    def __init__(self):
        """Initializes connection to database and parses command line arguments"""

        catalog.connect_database()
        catalog.clean_db()
        self.viewer = Viewer()
        self.editor = Editor()
   

    def arg_parser(self):
        """Parses command line arguments"""
        print

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()

        status = subparsers.add_parser('status')
        status.set_defaults(func=self.viewer.status)

        view_catalog = subparsers.add_parser('catalog')
        view_catalog.set_defaults(func=self.viewer.view_full_catalog)

        view_tags = subparsers.add_parser('tags')
        view_tags.add_argument('-a', '--alpha', action='store_true', help="List tags alphabetically")
        view_tags.set_defaults(func=self.viewer.view_all_tags)

        search = subparsers.add_parser('search')
        search.add_argument('-t', '--tags', nargs='+', required=True, help="Tags to search for")
        search.add_argument('-o', action='store_true', help="Search using 'or' logic ('and' logic by default)")
        search.set_defaults(func=self.viewer.search_tags)    

        add_file = subparsers.add_parser('addfile')
        add_file.add_argument('filename', help="Name of file to add catalog")
        add_file.set_defaults(func=self.editor.add_files)

        add_tags = subparsers.add_parser('addtags')
        add_tags.add_argument('filename', help="Name of file to add catalog")
        add_tags.add_argument('-t', '--tags', nargs='+', help="Tags to add to catalog")
        add_tags.set_defaults(func=self.editor.add_tag)

        edit_entry = subparsers.add_parser('edit')
        edit_entry.add_argument('filename', help="Name of file to add catalog")
        edit_entry.set_defaults(func=self.editor.edit_entry)

        clean_catalog = subparsers.add_parser('clean')
        clean_catalog.add_argument('-t', '--tags', nargs='+', help="Tags to be deleted from catalog entirely")
        clean_catalog.set_defaults(func=self.editor.clean_catalog)

        delete_entry = subparsers.add_parser('delete')
        delete_entry.add_argument('-f', '--file', required=True, help="File from which to delete specified tags")
        delete_entry.add_argument('-t', '--tags', nargs='+', help="Tags to be deleted")
        delete_entry.set_defaults(func=self.editor.delete_entry)

        merge_tags = subparsers.add_parser('merge')
        merge_tags.add_argument('--source', required=True, help="File from which tags are being taken")
        merge_tags.add_argument('--dest', required=True, help="Destination file to which tags from --source are added")
        merge_tags.set_defaults(func=self.editor.merge_tags)

 
        args = parser.parse_args()

        args.func(args)

def run():
    """Runs the program!"""
    
    connection = Connection()
    connection.arg_parser()



if __name__ == '__main__':
    
    run()
    


