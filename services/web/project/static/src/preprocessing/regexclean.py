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

        # print foundtext to console, control for length
        if len(foundtext) > 200:
            print('foundtext @',counter,' : ',foundtext[0:10], file=sys.stderr) # <-- uncomment to see in console
        else:
            print('foundtext @',counter,' : ',foundtext, file=sys.stderr) # <-- uncomment to see in console

        # filter visible text from foundtext
        visibletexts = list(filter(tagvisible, foundtext))

        # print visibletext to console, control for length
        if len(visibletexts) > 200:
            print('visibletexts @',counter,' : ',visibletexts[:10], file=sys.stderr) # <-- uncomment to see in console
        else:
            print('visibletexts @',counter,' : ',visibletexts, file=sys.stderr) # <-- uncomment to see in console

        # regex substitute all alphabetical characters
        regex_pattern = r'[^A-Za-z ]+' # <-- alpha characters only

        # if the filter took out all text due to no tags being present at all
        if len(visibletexts) == 0:
            # then do regex substitution on the original foundtext prior to filtering
            substitute_output = re.sub(regex_pattern, '', foundtext[0])
            # print current substitute output
            print('No visible text found. Substituting foundtext at index 0.', file=sys.stderr) # <-- uncomment to see in console

        # if the filter worked and there is still some values left
        elif len(visibletexts) >= 1:
            # if there is more than one visibletexts item
            if len(visibletexts) > 1:
                # join with spaces
                visibletextsjoined = " ".join(visibletexts)
                # print status to console
                print('len(visibletexts) >1, joining into string with spaces.', file=sys.stderr) # <-- uncomment to see in console
            else:
                # leave alone, grab first item
                visibletextsjoined = visibletexts[0]
                # print status to console
                print('len(visibletexts) == 1, using first index.', file=sys.stderr) # <-- uncomment to see in console

            # then do regex on joined item
            substitute_output = re.sub(regex_pattern, '', visibletextsjoined)
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
