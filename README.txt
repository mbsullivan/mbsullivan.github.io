This repo is a forest of sub-repos:

/ (root) is ssh://hg@bitbucket.org/mbsullivan/mbs954_academic_website
/framework/ is https://github.com/mbsullivan/www-pysub2
/structure/ is ssh://hg@bitbucket.org/ssully/academic_website_structure
/attachments/cv/ is git@github.com:mbsullivan/mbs954_cv
/attachments/resume/ is ssh://hg@bitbucket.org/mbsullivan/resume

Connecting to services:

(0) github

hg push github

(1) webspace

Connect to Server -> Secure WebDav -> webspace.utexas.edu/mbs954 -> fill in credentials

(2) lph (svn)

@ ~/svn_users/mbsullivan/

- then check in, will take 10-15 mins

Semi-structural files that differ:

- source/includes/head
