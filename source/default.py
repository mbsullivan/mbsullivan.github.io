"""

  HTML static substitution helper

  (c) 2013 Michael Sullivan

"""

import sys, os

def insert_file(fn, fldr):
    """ Insert the contents of a file. """
    # TODO: add in error reporting
    with open(os.path.join(fldr,fn)) as fh:
        fc = fh.read()
    return fc

def comment(*args, **kwargs):
    """ Take any number of arguments, and ignore them all.

    Used for making non-user-visible comments.

    """
    pass

if __name__ == "__main__":
    sys.exit("This is a supplementary file.")
