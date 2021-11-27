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
<details id="${bibpaper["ID"]}">
  <summary>
  % if bibpaper["ENTRYTYPE"] == "techreport":
${href_title(bibpaper)} (<span itemprop="datePublished">${bibpaper["year"]}</span>). <span itemprop="isPartOf">Technical report ${bibpaper["number"]}, LPH Group, Department of Electrical and Computer Engineering, The University of Texas at Austin</span>.
  % elif bibpaper["ENTRYTYPE"] == "phdthesis":
${href_title(bibpaper)} (<span itemprop="datePublished">${bibpaper["year"]}</span>). <span itemprop="isPartOf">PhD Dissertation, The University of Texas at Austin</span>.
  % else:
${href_title(bibpaper)} (<span itemprop="datePublished">${bibpaper["year"]}</span>). <span itemprop="isPartOf">${bibpaper["book"]}</span>. 
%endif
  </summary>
  <%

    def format_authors(author_list):
      """ Turns (surname, other) into (other, surname).

      """
      new_authors = []

      for author in author_list:
        split_names = author.split(",")
        if len(split_names) != 2:
          print("ERROR!")
          print(author_list)
        new_author = " ".join(split_names[::-1])

        # replace single characters with character+dot
        split_new_author = new_author.split(" ")
        for idx, author in enumerate(split_new_author):
          if len(split_new_author[idx]) == 1:
            split_new_author[idx] = split_new_author[idx] + "."
        post_split_new_author = " ".join(split_new_author)

        new_authors.append(post_split_new_author)

      return new_authors


    def insert_field(bibpaper, field):
      """ Either print a field + period or not, depending on if the field exists.

      """
      if field == "author":
        text = ", ".join(format_authors(bibpaper.get(field, [])))
      elif field == "booktitle":
        # italicize
        # TODO: get working with CSS sheets, etc
        if field in bibpaper:
          text = "In " + bibpaper[field]
        else:
          text = ""
      else:
        text = bibpaper.get(field, "")
      if text == "":
        return ""
      else:
        return text + ". "
  %>\
  <div class="elaboration">
    <dl>
      <dt>Full Citation</dt>
      <dd>
      ${insert_field(bibpaper, "author")}${insert_field(bibpaper, "year")}${insert_field(bibpaper, "title")}${insert_field(bibpaper, "booktitle")}${insert_field(bibpaper, "journal")}${insert_field(bibpaper, "pages")}
      </dd>
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
        <span itemprop="description">${post_filter(bibpaper["abstract"])}</span>
      </dd>
      <dt>BibTex</dt>
      <dd>
        ${href_bib_snippet(bibpaper)}
      </dd>
    </dl>
  </div>
</details>
</%def>\
