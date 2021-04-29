# import the dependencies
# google search
from googlesearch import search
# beautifulsoup
from bs4 import BeautifulSoup as bs
# requests
import requests


# define search functionality for application
def searchterms(search_term):
    # search the given input
    search_output = search(search_term, num_results=100)
    # output as a list of URLs
    # the first item search_results[0] is the Google Search string used
    search_results = search_output[1:(num_results+1)]
    # return a list of all search results
    return(search_results)

# define the scrape functionality for application
def scrapeurls(search_results):
    # index search results

    # start empty list of titles and texts
    textlist = []
    titlelist = []

    # for each search result through the length of search_results
    for counter in range(0,len(search_results)):
        # grab each URL
        url = search_results[counter]
        # get the url response
        url_response = requests.get(url)
        # return beautifulsoup html parser from response
        url_soup = bs(url_response.text, 'html.parser')
        # Title of the parsed page, append to list
        titlelist.append(url_soup.title)
        # find all text, append to list
        textlist.append(url_soup.find_all(text=True))

    # return the title and text
    return(titlelist,textlist)
