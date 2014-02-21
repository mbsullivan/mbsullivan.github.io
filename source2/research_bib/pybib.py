import os
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import *


# for generating clean bibtex snippets
def bib_customizations(record):
    """Use some functions delivered by the library
    :param record: a record
    :returns: -- customized record
    """
    record = page_double_hyphen(record)         # Separate pages by a
                                                # double hyphen (--)
    record = homogenize_latex_encoding(record)  # Homogeneize the latex
                                                # enconding style for bibtex
    return record

# for stripping out unprinted characters from the record
def strip_latex(record):
    """ Strip out unrendedered characters from the record
    :param record: a record
    :returns: -- customized record
    """
    def strip_key(record, key):
        """ If the key exists, strip it. """
        strip_maps = [("{", ""), ("}", ""),
                      ("\&", "&"), ("\%", "%")]
        if key in record:
            for strip_map in strip_maps:
                record[key] = record[key].replace(*strip_map)

    keys_to_strip = ["title", "abstract", "booktitle", "journal"]
    for key in keys_to_strip:
        strip_key(record, key)

    return record

# for pretty-printing to the web
def web_customizations(record):
    """Use some functions delivered by the library
    :param record: a record
    :returns: -- customized record
    """
    record = type(record)                 # Put the type into lower case
    record = author(record)               # Split author field into a list
                                          # of "Name, Surname"
    record = keyword(record)              # Split keyword field into a list
    record = page_double_hyphen(record)   # Separate pages by a double
                                          # hyphen (--)
    record = strip_latex(record)          # Strip out escaped Latex characters
    record = convert_to_unicode(record)   # Convert accent from latex to
                                          # unicode style
    return record

# for sorting

# months, in order (for sorting)
month_list = ["",
              "january",
              "february",
              "march",
              "april",
              "may",
              "june",
              "july",
              "august",
              "september",
              "october",
              "november",
              "december"]


def sort_key(entry):
    """ Returns a tuple for the multiple sorts to perform on
        a bibtex entry.
    """
    # year (mandatory)
    year = entry["year"]
    # month (optional)
    month = entry.get("month", "")
    monthnumber = month_list.index(month.lower())
    assert(monthnumber >= 0)    # detect abbreviated months
    # alphabetical
    name = entry["title"]

    # sorting by a tuple performs multiple sorts
    return (year, monthnumber, name)

def get_web_bib(params_obj, techreports=False):
    """ Return the parsed paper list, customized for web formatting.

        Split results between peer-reviewed and working publications.
    """
    with open(os.path.join(params_obj.BIB_FLDR, "research.bib"), "r") as bibfile:
        # parse bib file
        bp = BibTexParser(bibfile, customization=web_customizations)
        bplist = bp.get_entry_list()

        # separate out tech reports and peer-reviewed papers
        non_tr_bplist = [x for x in bplist if x["type"] != "techreport"]
        tr_bplist = [x for x in bplist if x["type"] == "techreport"]

        # sort results
        tgt_bplist = tr_bplist if techreports else non_tr_bplist
        sorted_by_year = sorted(tgt_bplist, key=sort_key, reverse=True)
        return sorted_by_year

def generalized_booktitle(paper):
    """ Return the book that a paper was found in, works for conferences and journals. """
    bt = paper.get("booktitle", None)
    bt = paper.get("journal", None) if bt is None else bt
    assert(bt is not None)
    return bt
