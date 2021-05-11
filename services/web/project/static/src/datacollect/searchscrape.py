# import the dependencies
# google search
from googlesearch import search
# beautifulsoup
from bs4 import BeautifulSoup as bs
# requests
import requests
import urllib.request
from urllib.request import Request, urlopen
from urllib.error import HTTPError
"""Database models."""
from project import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import Models
from project.static.data.rawdata.articlemodels import Article, Collection



# define search functionality for application
# gives dictinary list of urls
def searchterms(search_term):
    # set the results quantity
    resultsqty=10
    # search the given input
    search_output = search(search_term, num_results=resultsqty)
    # output as a list of URLs
    # the first item search_results[0] is the Google Search string used
    search_results = search_output[1:(resultsqty)+1]
    # return a list of all search results
    return(search_results)

# take in a dictionary list of urls
def scrapeurlsbyteresult(search_results):
    # index search results
    # start empty list of titles and texts
    textlist = []
    titlelist = []

    # set user agent for urlopen
    hdr = {'User-Agent': 'Mozilla/5.0'}
    # for each search result through the length of search_results
    for counter in range(0,len(search_results)):
        # grab each URL
        url = search_results[counter]
        # try reading the url response
        try:
            req = Request(url,headers=hdr)
            url_response = urllib.request.urlopen(req).read()
        except HTTPError as err:
            if err.code == 404:
                url_response = "404 Error"
            elif err.code == 403:
                url_response = "403 Error"
            else:
                url_response = "Other Error"

        # find all text, append to list
        textlist.append(url_response)

    # return the title and text as bytes object
    return(textlist)
