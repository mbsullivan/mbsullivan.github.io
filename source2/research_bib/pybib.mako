<%doc> 

    Mako helpers for formatting a bib file to HTML

    Assumes that params have been passed in the context, and that the
    research_bib folder and the includes folder is in the lookup paths.

</%doc>\
##
## a function for formatting a link to the pdf/page of a paper
<%def name="href_title(bibpaper)">\
% if "nopdf" in bibpaper:
${bibpaper["title"]}
% elif "link" in bibpaper:
<%
    # print error if the given URL is invalid
    from urllib2 import Request, urlopen, URLError
    req = Request(bibpaper["link"])
    try:
        response = urlopen(req)
    except URLError, e:
        p.error("URL %s seems to be invalid!" % bibpaper["link"])
%>
<a href="${bibpaper["link"]}">${bibpaper["title"]}</a>
% else:
<% 
    # form accessors for the harddrive and www (relative) paper paths
    import os
    hd_paper_pdf  = os.path.join(p.PAPERS_FLDR, bibpaper["id"] + ".pdf")
    www_paper_pdf = os.path.join(p.PAPERS_REL_FLDR, bibpaper["id"] + ".pdf")
    
    # check for the existance of the PDF, and report an error if it does not exist
    if not os.path.exists(hd_paper_pdf):
        p.error("PDF %s is linked to but does not exist!" % hd_paper_pdf)
%>
<a type="application/pdf" href="${www_paper_pdf}"/>${bibpaper["title"]}</a>
% endif
</%def>\
##
## a function for formatting a single paper
<%def name="apaper(bibpaper,techreport=False)">\
<details>
  <summary>
% if techreport is False:
    ${href_title(bibpaper)} (${bibpaper["year"]}). ${bibpaper["book"]}. 
% else:
    ${href_title(bibpaper)} (${bibpaper["year"]}). Technical report ${bibpaper["number"]}, LPH Group, Department of Electrical and Computer Engineering, The University of Texas at Austin.
%endif
  </summary>
  <div class="elaboration">
    <dl>
      <dt>Abstract</dt>
      <dd>
        ${bibpaper["abstract"]}
      </dd>
      <dt>BibTex</dt>
##      <dd><a type="text/plain" href="./attachments/papers/mrhu_lamar_2013.bib">A BibTex citation for the paper</a></dd>
    </dl>
  </div>
</details>
</%def>\
