# webscrape

## Overview

This readme file is an update from previous work done in May 2021.

The original readme file, which is really a string of research notes, can be found [here](readme_index/README_notes_01.md).

## Past Progress and Starting Up Again

### Previous Work

* The original source code in this app was created in early-May, 2021 and is at the time of writing this paragraph being restarted in mid-July 2021.
* There has been an approximately two month gap since last working with the application.

### Getting Up and Running

#### Building the Dockerfile

The application is built on docker with docker-compose, so getting it going uses the classic command set, while in the root project folder where the docker-compose.yml file sits:

```
$ sudo docker-compose up --build
```

Of course the name of the app or database may be shared with other running containers, so a shell script can be used to shut down all other containers in order to run the flask app and database from the webscrape code.

```
#!/usr/bin/env bash
echo "This script will exit immediately if a command exits with a non-zero status."
echo "The return value of the pipeline is the value of the last command to exit with a non-zero status."
set -euo pipefail

echo "Stopping all Docker Containers."
echo "stop $(docker ps -aq)"
docker stop $(docker ps -aq)

echo "Removing all Docker Containers."
echo "rm $(docker ps -aq)"
docker rm $(docker ps -aq)
```

More useful shell scripts can be found under [this repo](https://github.com/pwdel/dockerlubuntu).

#### Dealing with Any Errors

* One error came up during the build, the Google Search plugin requirement seems to have been updated as of June 9th, 2021. Previously the release was, "2020.0.2" and it is now, [1.0.1](https://pypi.org/project/googlesearch-python/1.0.1/).  The new version was added to the requirements.txt file as, "googlesearch-python" with no version.

#### Running the Local Web Program, Testing Functionality

After successfully running the docker container, the app can be found at 172.20.0.3:5000.  After logging in the user is presented with a dashboard that contains a, "Create Knowledgebase," option.

![](/readme_img/20210722_update_01.png)

Upon clicking, "Create Knowledgebase," the user is lead to a search bar into which they may enter a desired topic to begin a search process.

![](/readme_img/20210722_update_02.png)

##### Errors Found and Explination

Attempting the search, we get the following error:

```
NameError: name 'scrapeurls' is not defined
```

Upon further inspection, 'scrapeurls' is a depricated function, because in previous work it was found that another function we created:

> textfromhtml function requires a bytes object as an input,

Therfore, the function 'scrapeurlsbyteresult' has been created and used instead. It is likely that these function were being accessed through the flask shell rather than through the web interface for expediency, so the web interface was not updated.

The function flow goes as follows, in theory:

1. route.py -> searchstring = form.search.data
2. searchresults = searchterms(searchstring)
3. # scrape urls raw:
4. urlscrapes = scrapeurlsbyteresult(search_results)
5. textfromhtml(urlscrapes) --> return(extractedtexts,extractedtitles)

...which then get transferred into the database.

Presumably, these functions have been accessed through the flask shell via development mode, and the database has been inspected via the Postgres shell for expediency purposes.

##### Review on Flask Shell

To get into the flask shell:

1. Log into the docker container (which is really like remoting into a linux machine) via:

```
$ sudo docker exec -it flask /bin/bash
```
2. Then gain entry to the shell with:

```
flask shell
```

Once in the flask shell, function commands can be executed.  First though, you must import the function call by project structure as follows:

```
>>> from project.static.src.datacollect.searchscrape import searchterms, scrapeurlsbyteresult
>>> searchstring = "thus spoke zarathustra"
>>> search_results = searchterms(searchstring)
```
The output of searchterms is a list, as shown:

```
['https://www.amazon.com/Spake-Zarathustra-Dover-Thrift-Editions/dp/0486406636', 'https://www.amazon.com/Thus-Spoke-Zarathustra-Modern-Library/dp/0679601759', 'https://www.goodreads.com/book/show/51893.Thus_Spoke_Zarathustra', 'https://www.gutenberg.org/files/1998/1998-h/1998-h.htm', 'https://www.britannica.com/topic/Thus-Spake-Zarathustra', 'https://www.penguinrandomhouse.com/books/121945/thus-spoke-zarathustra-by-friedrich-nietzsche/', 'https://www.penguinrandomhouse.com/books/322953/thus-spoke-zarathustra-by-friedrich-nietzsche-translated-with-an-introduction-and-notes-by-r-j-hollingdale/', 'http://users.clas.ufl.edu/burt/LoserLit/zarathustra.pdf', 'https://books.google.com/books/about/Thus_Spake_Zarathustra.html?id=5IURAAAAYAAJ&printsec=frontcover&source=kp_read_button&newbks=1&newbks_redir=1']
```
That list can then be put into scrapeurlsbyteresult() to produce urlscrapes. Remember we have to import all functions by project structure (which we already did above).

```
>>> from project.static.src.datacollect.searchscrape import searchterms, scrapeurlsbyteresult
>>> urlscrapes = scrapeurlsbyteresult(search_results)
```
The output will be a list of text corresponding to each URL.

```
>>> from project.static.src.preprocessing.regexclean import textfromhtml, tagvisible
>>> extractedtexts,extractedtitles = textfromhtml(urlscrapes)
```
The output, extractedtexts,extractedtitles are lists. However due to the highly irregular nature of web scraping, much work is still needed on textfromhtml() to make this work in a variety of situations, this work includes both error handling as well as regex work.

### Cleaning Up textfromhtml()
