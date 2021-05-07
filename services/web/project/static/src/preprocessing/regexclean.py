# regex removal
import re
# BeautifulSoup
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request


# compile int a regular expression object given instructions
# remove first layer of tags, characters
htmltags_re = re.compile(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]')
# compile and remove newline tags
htmltags_nre = re.compile(r'\n\\n')

# empty text tags removed list
text_tagsremovedlist = []

# removetags function
# input a list of scraped websites, output text with regex removed
def removetags(urlscrapes):
    # urlscrapes is a tuple and is accessed by
    # urlscrapes[0] = title
    # urlscrapes[1] = text
    # do this for all items in text list
    for counter in range(0,len(urlscrapes[1])):
        # remove characters for a particular textlist item
        text_htmltags_removed = htmltags_re.sub('', str(urlscrapes[1][counter]))
        # remove newline function on that list item
        text_ntags_removed = htmltags_nre.sub('', text_htmltags_removed)
        # append to list
        text_tagsremovedlist.append(text_ntags_removed)

    return(text_tagsremovedlist)

# define tag_visible function for filter
# used in text_from_html function
def tagvisible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


# extract text from html body
def textfromhtml(urlscrapes):
    # set empty text append list to return filled
    extractedtexts = []
    # urlscrapes is a tuple and is accessed by: urlscrapes[0] = title, urlscrapes[1] = text
    # do this for all items in text list
    for counter in range(0,len(urlscrapes)-1):
        # grab the body of html text for a particular iteration
        body = urlscrapes[counter]
        # use the html parser to create a beautifulsoup object
        # note in our previous raw data extraction we had not used html.parser
        soup = BeautifulSoup(body, 'html.parser')
        # find all text within the beautifulsoup object
        foundtext = soup.findAll(text=True)
        # filter visible text from foundtext
        visibletexts = filter(tagvisible, foundtext)
        # append to extracted texts list
        extractedtexts.append(u" ".join(t.strip() for t in visibletexts))

    # return extractedtexts object
    return(extractedtexts)
