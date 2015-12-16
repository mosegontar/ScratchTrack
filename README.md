# ScratchTrack
A small command line program for browsing and tagging local files. (Ideally suited for keeping track of directories with many small miscellaneous files)

Scratch Track is written in Python 2.7 and uses the Peewee ORM. It was written to help me keep track of the many informal/throwaway
scripts and text files I have been generating while learning python. It was also a helpful way to introduce myself to databases.


##Running ScratchTrack:
Download the files and either add ScratchTrack to your PATH to run it from anywhere, or place it in some other directory on your computer and run it by entering `python /your/path/scratchtrack.py`.

ScratchTrack will create an appropriately named database file for your current working directory. 

For example, if you would like to keep track of the contents of your "Misc_Scripts" folder, make sure that folder is your current working directory, and then run ScratchTrack. A database file named 'misc_scripts_st.db' will then be created and it will keep track of that directory's contents. Whenever you want to browse the Misc_Scripts ScratchTrack database, just navigate to the Misc_Scripts directory and run ScratchTrack.


##Usage:

    -d: Delete Entry
    
        USAGE:
        -d                       : Shows valid deletion usages
        -d > file_name > tag(s). : delete tag(s) from file                           
        -d > *f > file_name(s)   : delete file from catalog
        -d > *t > tag(s)         : delete tag from catalog entirely; removes associations
        -d > **f                 : delete files in catalog that are not in CWD
  
    -e: Edit Entry Description
    
        USAGE:
        -e 
        -e > file_name1, file_name2,... : edit description of file(s)
    
    -f: Adds file name to database
    
    -h: Help Menu
    
    -m: Merge Tags
    
        USAGE:
        -m :               : Launch Merge Entry Menu. 
        -m > file1 > file2 : Add tags from file1 to file2`
        
    -s: Search for Tags
    
        USAGE:
        -s                       : launches search menu
        -s > and > tag1, tag2... : search for tag(s) using OR logic
        -s > or > tag1, tag2...  : search for tag(s) using AND logic
            
    -t: Add Tag to File
    
        USAGE:
        -t                             : launches add_tag menu
        -t > filename > tag1, tag2,... : adds tags to file entry
        
    -u: Displays new files in CWD if found and old files in catalog if found
    
    -v: View Catalog Entries
    
        USAGE:
        -v         : view all entries in catalog
        -v > alpha : view tags, sorted alphabetically
        -v > count : view tags, sorted by popularity
        
