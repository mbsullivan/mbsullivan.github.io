"""

  HTML static substitution helper

  (c) 2013 Michael Sullivan

"""

import sys, os

def threeway_file_split(filename):
    """ Split the filename into [path, rootname, ext]. """
    (path, filetail) = os.path.split(filename)
    (rootname, ext) = os.path.splitext(filetail)
    return (path, rootname, ext)

def insert_file(fn, fldr):
    """ Insert the contents of a file. """
    # TODO: add in error reporting
    with open(os.path.join(fldr,fn)) as fh:
        fc = fh.read()
    return fc

def menu_rreplace(s, tgt, rep_tgt):
    """ Reverse replacement of a string. """
    global menu_inserted
    menu_inserted = False
    new_s = s[::-1].replace(tgt[::-1], rep_tgt[::-1], 1)[::-1]
    # flag a menu insertion
    if new_s != s:
        menu_inserted = True
    return new_s


def insert_modified_header(this_file, fldr, header_file = "header", **kwargs):
    """ Insert the contents of the header file,
        modified to insert the active class. """
    # find file components
    (this_fldr, this_root, this_ext) = threeway_file_split(this_file)
    # get header
    with open(os.path.join(fldr,header_file)) as fh:
        fc = fh.read()
    # insert active class
    tgt = "href=\"%s%s\"" % (this_root, this_ext)
    return menu_rreplace(fc, tgt, tgt + " class=\"active\"")

def comment(*args, **kwargs):
    """ Take any number of arguments, and ignore them all.

    Used for making non-user-visible comments.

    """
    pass

if __name__ == "__main__":
    sys.exit("This is a supplementary file.")
