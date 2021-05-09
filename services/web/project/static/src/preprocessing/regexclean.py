# regex removal
import re
# BeautifulSoup
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

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
    extractedtitles = []
    # urlscrapes is a tuple and is accessed by: urlscrapes[0] = title, urlscrapes[1] = text
    # do this for all items in text list
    for counter in range(0,len(urlscrapes)):
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
        # find title
        title = soup.find('title')
        # append title
        extractedtitles.append(title.string)

    # return extractedtexts object
    return(extractedtexts,extractedtitles)
