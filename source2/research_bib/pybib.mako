<%doc> 

    Mako helpers for formatting a bib file to HTML

    Assumes that params have been passed in the context, and that the
    research_bib folder and the includes folder is in the lookup paths.

</%doc>\
##
## a function for formatting a link to the pdf/page of a paper
<%def name="href_title(bibpaper)">\
<div itemscope itemtype="http://schema.org/ScholarlyArticle">
% if "nopdf" in bibpaper:
<span itemprop="name headline">${bibpaper["title"]}</span>
% elif "link" in bibpaper:
<%
    # NOTE 2/10/15: hangs, so I'm taking it out
    # # print error if the given URL is invalid
    # from urllib2 import Request, urlopen, URLError
    # req = Request(bibpaper["link"])
    # try:
    #     response = urlopen(req)
    # except URLError, e:
    #     p.error("URL %s seems to be invalid!" % bibpaper["link"])
%>
<a itemprop="image" href="${bibpaper["link"]}"><span itemprop="name headline">${bibpaper["title"]}</span></a>
% else:
<% 
    # form accessors for the harddrive and www (relative) paper paths
    import os
    hd_paper_pdf  = os.path.join(p.PAPERS_FLDR, bibpaper["id"] + p.EXT_PDF_OUT)
    www_paper_pdf = os.path.join(p.PAPERS_REL_FLDR, bibpaper["id"] + p.EXT_PDF_OUT)
    
    # check for the existance of the PDF, and report an error if it does not exist
    if not os.path.exists(hd_paper_pdf):
        p.error("PDF %s is linked to but does not exist!" % hd_paper_pdf)
%>
<a itemprop="image" type="application/pdf" href="${www_paper_pdf}"/><span itemprop="name headline">${bibpaper["title"]}</span></a>
% endif
</%def>\
##
## a function for formatting a link to the bibtex snippet of a paper
<%def name="href_bib_snippet(bibpaper)">\
<% 
    # form accessors for the harddrive and www (relative) paper paths
    import os
    hd_bib_snippet  = os.path.join(p.BIBS_FLDR, bibpaper["id"] + p.EXT_BIB_OUT)
    www_bib_snippet = os.path.join(p.BIBS_REL_FLDR, bibpaper["id"] + p.EXT_BIB_OUT)
    
    # check for the existance of the bib snippet, and report an error if it does not exist
    if not os.path.exists(hd_bib_snippet):
        p.error("Bibtex snippet %s is linked to but does not exist!" % hd_bib_snippet)
%>
<a type="text/plain" href="${www_bib_snippet}">A BibTex citation for the paper</a>
</div>
</%def>\
