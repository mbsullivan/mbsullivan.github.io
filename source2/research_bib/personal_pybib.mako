<%doc> 

    Personalized Mako helpers for formatting a bib file to HTML

    Assumes that params have been passed in the context, and that the
    research_bib folder and the includes folder is in the lookup paths.

</%doc>\
##
## more generic helper functions
<%namespace file="pybib.mako" import="*"/>
##
## a function for formatting a single paper
<%def name="apaper(bibpaper)">\
<details>
  <summary>
% if bibpaper["type"] != "techreport":
    ${href_title(bibpaper)} (${bibpaper["year"]}). ${bibpaper["book"]}. 
% else:
    ${href_title(bibpaper)} (${bibpaper["year"]}). Technical report ${bibpaper["number"]}, LPH Group, Department of Electrical and Computer Engineering, The University of Texas at Austin.
%endif
  </summary>
  <div class="elaboration">
    <dl>
      <dt>Abstract</dt>
      <dd>
<%
    def post_filter(text):
        """ Maintain endlines in HTML.
        
        """
        # eliminate leading and trailing white space altogether
        trimmed_text = text.strip()
        split_text = trimmed_text.split("\n")
        return "<br />".join(split_text)
%>\
        ${post_filter(bibpaper["abstract"])}
      </dd>
      <dt>BibTex</dt>
      <dd>
        ${href_bib_snippet(bibpaper)}
      </dd>
    </dl>
  </div>
</details>
</%def>\
