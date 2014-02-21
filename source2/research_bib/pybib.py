from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import *


# Let's define a function to customize our entries.
# It takes a record and return this record.
def customizations(record):
    """Use some functions delivered by the library
    :param record: a record
    :returns: -- customized record
    """
    record = type(record)
    record = author(record)
    record = editor(record)
    record = journal(record)
    record = keyword(record)
    record = link(record)
    record = page_double_hyphen(record)
    record = doi(record)
    record = convert_to_unicode(record)
    return record

with open("research.bib", "r") as bibfile:
    bp = BibTexParser(bibfile, customization=customizations)
    print bp.get_entry_list()[0]
    """for authorlist in [x.get(u'author', "") for x in bp.get_entry_list()]:
        print authorlist
    print "\n==========\n"
    for authorlist in [x.get(u'author', "") for x in bp.get_entry_list()]:
        print getnames(authorlist)"""
