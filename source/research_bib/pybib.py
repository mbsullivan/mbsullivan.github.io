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
    return record


# for adding a general "book" field to peer-reviewed works
def general_booktitle(record):
    """ Add the book that a paper was found in.

        Works for conferences and journals. """
    bt = record.get("booktitle", None)
    bt = record.get("journal", None) if bt is None else bt
    if bt is not None:
        record["book"] = bt

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
    record = general_booktitle(record)    # Add the generic "book" field to
                                          # peer-reviewed publications
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


def sort_only_year(entry):
    """ Returns a tuple for the multiple sorts to perform on
        a bibtex entry.
    """
    # year (mandatory)
    year = entry["year"]

    return year


# subsetted records, in order (for sorting)
record_field_list = ["author",
                     "title",
                     "booktitle",
                     "journal",
                     "volume",
                     "pages",
                     "number",
                     "institution",
                     "month",
                     "year",
                     "location",
                     "url"]


def create_bibtex_snippet(params_obj, record):
    """ Subset the record and create a bibtex snippet on disk. """
    out_file_path = os.path.join(params_obj.BIBS_FLDR,
                                 record["ID"] + params_obj.EXT_BIB_OUT)
    with open(out_file_path, "w") as bib_snippet_file:
        # bibtex header
        bib_snippet_file.write("@%s {%s,\n" % (record["ENTRYTYPE"], record["ID"]))

        # find each subsetted field, in order
        subsetted_fields = [(key, value) for key,value in record.items()
                            if key in record_field_list]      # subset fields
        subsetted_fields.sort(key=lambda x: record_field_list.index(x[0]))

        # print all formatted key = value lines into record
        for field in subsetted_fields:
            bib_snippet_file.write("%s%s = {%s},\n" % ((params_obj.BIB_INDENT,)
                                                    + field))

        # bibtex footer
        bib_snippet_file.write("}\n")


def get_web_bib(params_obj, create_bib_snippets=False):
    """ Return the parsed paper list, customized for web formatting.

        If create_bib_snippet is True, generate a subsetted bibtex snippet. """
    weblist = []    # web formatted
    biblist = []    # bib formatted
    # open and parse all bibfiles (web format)
    for bib_filetail in params_obj.BIB_FILES:
        with open(os.path.join(params_obj.BIB_FLDR, bib_filetail), "r") as bibfile:
            bibfile_str = bibfile.read()

            # parse bib file for web
            webparse = BibTexParser(bibfile_str, customization=web_customizations)
            weblist += webparse.get_entry_list()

            # parse bib file for bib snippets
            bibfile.seek(0)     # rewind
            bibparse = BibTexParser(bibfile_str, customization=bib_customizations)
            biblist += bibparse.get_entry_list()

    # if required, create bib snippets for each record
    if create_bib_snippets:
        for record in biblist:
            create_bibtex_snippet(params_obj, record)

    # return web-formatted version
    sorted_asc = sorted(weblist, key=sort_key)  # ascending by year and name
    sorted_by_year = sorted(sorted_asc, key=sort_only_year, reverse=True)

    return sorted_by_year
