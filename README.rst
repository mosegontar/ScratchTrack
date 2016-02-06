*************
Scratch Track
*************

Scratch Track is a simple command line program for tagging and tracking files in your local directories. It was motived by the desire to keep track of scratch files I was generating while learning Python.

When it's run, Scratch Track creates a hidden .db file in your current working directory (named '.the_name_of_your_cwd_st.db'). 

Installation from source:

.. code:: bash

    git clone https://github.com/mosegontar/ScratchTrack.git
    python install setup.py

=====
Usage
=====

Get help!

.. code:: bash

    strack [-h]

Check which files in your CWD are not in the directory's Scratch Track catalog:

.. code:: bash

    strack status

Add a file as an entry and a description to the catalog:

.. code:: bash

    strack addfile file_name

Tag a file!

.. code:: bash

    strack addtags file_name -t tag1 tag2 'tag 3'

View all entries in the catalog:

.. code:: bash

    strack catalog

View a list of all tags (default sort by count, optional argument -a sorts alphabetically):

.. code:: bash

    strack tags [-a]


