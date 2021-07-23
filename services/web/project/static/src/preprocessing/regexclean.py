# regex removal
import re
# sys for console print tools
import sys
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
        visibletexts = list(filter(tagvisible, foundtext))

        # print to console
        print('visibletexts @',counter,' : ',visibletexts[:200], file=sys.stderr)

        # regex substitute all alphabetical characters
        regex_pattern = r'[^A-Za-z ]+' # <-- alpha characters only

        # if the filter took out all text due to no tags being present at all
        if len(visibletexts) == 0:
            # then do regex substitution on the original foundtext prior to filtering
            substitute_output = re.sub(regex_pattern, '', foundtext[0])
            # print current substitute output
        # if the filter worked and there is still some values left
        elif len(visibletexts) == 1:
            # then do regex on the list item
            substitute_output = re.sub(regex_pattern, '', visibletexts[0])
            print(visibletexts[0])
            pass
        else:
            substitute_output = "Does not fit visible text requirement for unknown reason."

        # append to extracted texts
        extractedtexts.append(substitute_output)

        # find title
        title = soup.find('title')
        try:
            # append title
            extractedtitles.append(title.string)
        except:
            # if erropr just append "Error"
            extractedtitles.append("Title Error")

    # return extractedtexts object
    return(extractedtexts,extractedtitles)
