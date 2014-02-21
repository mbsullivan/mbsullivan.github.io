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

with open("research.bib", "r") as bibfile:
    bp = BibTexParser(bibfile, customization=web_customizations)
    bplist = bp.get_entry_list()
    sorted_by_year = sorted(bplist, key=sort_key, reverse=True)
