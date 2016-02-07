*************
Scratch Track
*************

Scratch Track is a simple command line program for tagging and tracking files in your local directories. It was motived by the desire to keep track of the many scratch files I was generating while learning Python.

When it's run, Scratch Track creates a hidden .db file in your current working directory (named '.the_name_of_your_cwd_st.db'). You can then add files to this 'catalog', allowing you to keep track of your files, tag them, and search for specific files by querying tags. 

Installation from source:

.. code:: bash

    git clone https://github.com/mosegontar/ScratchTrack.git
    python install setup.py

=====
Usage
=====

Get help and usage directions!

.. code:: bash

    strack [-h]

Check which files in your CWD are not in the directory's Scratch Track catalog:

.. code:: bash

    strack status

Add a file as an entry and a description to the catalog:

.. code:: bash

    strack addfile file_name

View all entries in the catalog:

.. code:: bash

    strack catalog    

Tag a file!

.. code:: bash

    strack addtags file_name -t tag1 [tag2 'tag 3' ...]

Merge tags from one file (the 'source') with those of another (the 'destination'):

.. code:: bash

    strack merge --source file_name1 --dest file_name2 

View a list of all tags (default sort by count, optional argument -a sorts alphabetically):

.. code:: bash

    strack tags [-a]

Search for files based on tag queries (default search uses AND operator, but option [-o] uses operator ): 

.. code:: bash

    strack search -t tag1 [tag2 ...] [-o]

Edit an existing catalog file's description:

.. code:: bash

    strack edit file_name

Remove all expired entries from catalog. If option [-t] used, removes listed tags from catalog entirely

.. code:: bash

    strack clean [-t tag1 [tag2 ... ]]

Delete a specific file from catalog. If option [-t] used, the file remains in the catalog but listed tags are no longer associated with that file.

.. code:: bash

    strack delete file_name [-t tag1 [tag2 ...]]





