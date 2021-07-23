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
from project.static.src.datacollect.searchscrape import searchterms, scrapeurlsbyteresult
urlscrapes = scrapeurlsbyteresult(search_results)
```
The output will be a list of text corresponding to each URL.

```
>>> from project.static.src.preprocessing.regexclean import textfromhtml, tagvisible
>>> extractedtexts,extractedtitles = textfromhtml(urlscrapes)
```
The output, extractedtexts,extractedtitles are lists. However due to the highly irregular nature of web scraping, much work is still needed on textfromhtml() to make this work in a variety of situations, this work includes both error handling as well as regex work.

### Cleaning Up textfromhtml()

The function is fundamentally a for loop:

```
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

```

Currently if there is no found text, there is a AttributeError: 'NoneType' object has no attribute 'string' error on:

```
extractedtitles.append(title.string)
```
Basically, no title is found from beautifulsoup, which means this should be a try/except clause with a default item to add in the case that nothing can be extracted for a given element.

To solve this issue, we use try/except:

```
try:
		# append title
		extractedtitles.append(title.string)
except:
		extractedtitles.append("Title Error")
```

However, note that even with this fix we still get the following:

> Some characters could not be decoded, and were replaced with REPLACEMENT CHARACTER.

For the titles we have the following list (new line added for each element for visibility):

```
[
'Also sprach Zarathustra - Wikipedia',
'Amazon.com: Thus Spake Zarathustra (Dover Thrift Editions) (9780486406633): Friedrich Nietzsche, Thomas Common: Books', 'Thus Spoke Zarathustra: A Book for All and None (Modern Library (Hardcover)): Nietzsche, Friedrich, Kaufmann, Walter: 9780679601753: Amazon.com: Books',
'Thus Spoke Zarathustra by Friedrich Nietzsche',
'\r\n      Thus Spake Zarathustra, by Friedrich Nietzsche\r\n    ',
'Thus Spake Zarathustra | treatise by Nietzsche | Britannica', 'Thus Spoke Zarathustra by Friedrich Nietzsche: 9780679601753 | PenguinRandomHouse.com: Books',
'Error',
'Thus Spake Zarathustra: a book for all and none - Friedrich Wilhelm Nietzsche - Google Books'
]
```
However for the variable, "extractedtexts" we get a lot of symbols which are not text.  This is where an actual functioning regex would come in handy.

```
# grab the body of html text for a particular iteration
body = urlscrapes[counter]
# use the html parser to create a beautifulsoup object
# note in our previous raw data extraction we had not used html.parser
soup = BeautifulSoup(body, 'html.parser')
# find all text within the beautifulsoup object
foundtext = soup.findAll(text=True)
# filter visible text from foundtext
visibletexts = filter(tagvisible, foundtext)
# regex substitute all alphabetical characters
regex_pattern = r'[^A-Za-z ]+' # <-- alpha characters only
# substituted texts, removing based upon regex pattern
substitute_output = re.sub(regex_pattern, '', visibletexts)
# append to extracted texts list
extractedtexts.append(u" ".join(t.strip() for t in substitute_output))

```

The key regex we used here, which appears to clean up a lot, but not everything is:

```
regex_pattern = r'[^A-Za-z ]+' # <-- alpha characters only
```

This pattern, when combined with re.sub, finds all non-alphabetical characters in visibletexts and turns them into nothing, or ''.

Side note - one problem with building this, is that re-building any static code requires completely stopping and re-starting flask, and subsequently importing any functions we re-built.

Currently, our import tasks are:

```
from project.static.src.datacollect.searchscrape import searchterms, scrapeurlsbyteresult
from project.static.src.preprocessing.regexclean import textfromhtml, tagvisible
```

While the commands we need to run to test this out are:

```
searchstring = "thus spoke zarathustra"
search_results = searchterms(searchstring)
urlscrapes = scrapeurlsbyteresult(search_results)
extractedtexts,extractedtitles = textfromhtml(urlscrapes)
```
Upon attempting this after adding in the regex expression above we get the following error:

```
extractedtexts,extractedtitles = textfromhtml(urlscrapes)
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/usr/src/theapp/project/static/src/preprocessing/regexclean.py", line 37, in textfromhtml
    substitute_output = re.sub(regex_pattern, '', visibletexts)
  File "/usr/local/lib/python3.8/re.py", line 210, in sub
    return _compile(pattern, flags).sub(repl, string, count)
TypeError: expected string or bytes-like object
```
Basically, the output of foundtext and filter (visibletext) is likely a filter object, rather than a string, which the regex cleaner is looking for.  Moreover, there are different cases of text that we might encounter from the web. The below code is an attempt to account for two cases:

```
# regex substitute all alphabetical characters
regex_pattern = r'[^A-Za-z ]+' # <-- alpha characters only

# if the filter took out all text due to no tags being present at all
if len(visibletexts) == 0:
    # then do regex substitution on the original foundtext prior to filtering
    substitute_output = re.sub(regex_pattern, '', foundtext[0])    
    print(foundtext[0])
    pass
# if the filter worked and there is still some values left
elif len(visibletexts) == 1:
    # then do regex on the list item
    substitute_output = re.sub(regex_pattern, '', visibletexts[0])
    print(visibletexts[0])
    pass
else:
    substitute_output = "Does not fit visible text requirement for unknown reason."

```

Further testing may be needed to identify more cases and sleuth how to more efficiently scrape from the web. The following private Colab notebook has been set up to run experiments:

[Colab on Webscrape Regex](https://colab.research.google.com/drive/1BMUqBCTWU9v3UVYcEu6_H6nNkajSwmyB#scrollTo=qxFO8x8cavVw)

After testing the above in our dev environment, we get another error:

```
TypeError: object of type 'filter' has no len()
```
This is simply because we had to add list(filter()) on the filter function to convert the object into a list.

After running this new code, we get:

```
extractedtexts
[]
```

Basically, the extractedtexts is now empty.
