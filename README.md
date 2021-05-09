# webscrape

# Overview

# Creating a Folder Structure

## Storing the Data and Raw Data

Generally described, machine text generation is a series of mathematical transforms performed on words or parts of speech (groups of words) which have been assigned numbers or identifiers and whose order or the order of those numbers identified. The ability to generate new, open-ended text is loosely based upon, "vocabularies" which are essentially collections of words or tokens.

There are many different types of transforms and ways of performing machine text generation depending upon the end result, but in the abstract a flow chart like the following examples is performed:

![](/readme_img/NLP-flowchart.png)

Source: [3M Inside Angle](https://www.3mhisinsideangle.com/blog-post/amia-2017-learning-showcase-terminology-enabled-clinical-natural-language-processing-unstructured-information-extraction/)

![](/readme_img/NLG-flowchart.png)

Source: ![](https://www.degruyter.com/document/doi/10.1515/jisys-2018-0291/html)

From a user perspective, one of the most time consuming parts of generating language is building a base of material from which to, "specialize" in a topic area.  Essentially, topic areas of expertise in language differ from one another, the terms, buzzwords and perhaps acronyms differ from industry to industry or domain to domain. An article may need to maintain a certain semantic or "vocabularistic," decorum in order to sound somewhat credible, or perhaps differently stated, to have a voice that sounds plausible.

From that perspective, it would be nice to be able to build vocabulary bases over time, perhaps combine them together into groups of vocabularies, which we might call a, "knowledgebase" and automatically generate text based upon a knowledgebase, which is really just a collection of specialized vocabularies in a particular area.

When a new article gets generated, the user should have the capability to, "attach" a knowledgebase to the article the user wants to create, in order to customize the article and have the article move forward in the direction the user wants it to go.

Fundamental texts or articles where these, "vocabularies" come from may also need to be either selected from online sources or uploaded.

With that type of feature set, there is a need for different sets of raw data, which can be dynamically selected by a user to generate vocabularies, or to generate knowledge bases upon which articles are created.

Hence, a relational database model comes to mind which could help manage all of this:

![](/readme_img/knowledgebases1.png)

Expanding upon this, there are certain, "stops" within the, "Article -> Vocabulary -> Knowledgebase" Pipeline. Breaking it down:

* Articles have, "raw text" which can be cleaned up and have regex expressions removed, turning them into, "regexremoved."
* Vocabularies can basically be, "tokenized" versions of the, "regexremoved" data, essentially creating objects which are ready to add into, "knowledgebases."
* Hence knowledgebases are simply collections of pre-tokenized, regex-cleaned raw text collected from articles.

## Storing Machine Learning Models

Whereas with GPT2 in a previous project, [SRCFlask](https://github.com/pwdel/srcflask), the GPT2 head model was invoked and "fine tuned," on a small set of text, predicting the next logical few tokens in a string based upon a search model, it is possible to actually encode text using BERT as a language Machine Learning model rather than GPT.  There are a variety language models, including ElMo, which is more open source but possibly less capable than BERT, which actually allow building out and customizing open-ended text generation based upon custom vocabularies.

At some point, decisions may need to be made about where to store actual pre-built models, (e.g. trained models) in order to make the process of fine-tuning or invoking models much faster and less resource dependent. We will go through that in the future, as for now the purpose is to build out more of a web scrapting architecture which will enable future vocabulary generation.

## Project Structure

From the, "flask src" project, we had the overall project structure:

```
└── src
│	├── features
│	├── preperation
│	├── preprocessing
│	├── evaluation
│	└──	js
└── tests
│	└──	unit_tests
└── models
│	├── seedmodels
│	└──	retrainedmodels
└── data
│	├──	raw_data
│	├──	processed_data
│	└──	user_input_data
└── pipeline
│	└──	model_retraining_automation_scripts
└── docs
	├──	Documentation
	└──	Notebooks
```

Looking at our above data, we can fairly naturally find where to put models which help build out the above relational database.

```
└── data
│	  ├──	init.py
│	├──	raw_data
│	    ├──	init.py
│	    └── articlemodels.py
│	├──	processed_data
│	    ├──	init.py
│	    └── vocabmodels.py
│	└──	user_input_data
```

* Articles are raw data, so all of the information contained in articlemodels.py has to do with raw text and regex-cleaned text, which for our purposes is raw data.
* Vocabularies are processed, meaning tokenized, and no longer raw, so anything dealing with Vocabularies, as well as Knowledgebases and Holdings can go into this file.

As far as the actual python work and lifting, this could be built into the following files:

```
└── src
│	  ├── features
│	    ├──	init.py
│ 	  └──	articletokenize.py
│	  ├── preperation
│	    ├──	init.py
│ 	  └──	knowledgebasebuild.py
│ 	├── preprocessing
│	    ├──	init.py
│ 	  └──	regexclean.py
│	  ├── evaluation
│ 	└──	js
```

* tokenize.py -
* knowledgebasebuild.py
* regexclean.py

### Brief Term Definitions - Features vs. Preparation vs Pre-processing

#### Pre-processing

* Dealing with missing data, noisy data or inconsistent data. Basically this deals with, "cleaning the data," so that we can start to analyze it in some form.
* In the case of text analysis, this may involve removing common repeating words, removing punctuation, or a variety of other methods. The algorithms we are working with, such as BERT have their own embedded ways of masking words, so technically that would fall under pre-processing, but for our application we may call on BERT within a different function.

#### Preperation

* Data preperation happens after pre-processing.
* This may involve additional cleaning missing or noisy data, tranformations, normalization, aggregation, and data reduction, basically scaling things to make it more processable.

#### Wrangling

* Data wrangling includes recalculating the data  for cross validation (for example normalizing numbers, scaling numbers, projecting matricies, removing outliers), and dividing the dataset up into training data and test data.

The process of Pre-processing, Preperation, and Wrangling is sort of like Extract, Transform and Load in the IT world of data warehousing. However instead of a data warehouse, we're just working with whatever database.

## Building the Webscrape Algorithm and Layout

### Project Structure

From our project structure above:

```
└── data
│	  ├──	init.py
│	  ├──	raw_data
│	      ├──	init.py
│	      └── articlemodels.py
│	  ├──	processed_data
│	      ├──	init.py
│	      ├── vocabmodels.py
│	      └── knowledgebasemodels.py
│	  └──	user_input_data
```


### Fundamentals of Webscraping

The code for how the physical web scraping part of this project can be accomplished has been more or less built out at [this Google Colab Notebook](https://colab.research.google.com/drive/1fuN-rt7wA4gavo-AdZR5Uzr6w41_2kEh#scrollTo=emOI5-9dtvwp).

Essentially, the following is done:

1. Perform a Search on a Given Term.
2. Go through the URL's one by one and read the raw text. Put the raw text into the database. There are several ways to extract the raw text.
3. Remove regex (this is a pre-processing routine).
4. Put the fully cleaned raw text in a database for later usage.

### Sponsor Search Capability

Search can simply be a form fill, with some written tips on what kinds of topics to search for, and for what purpose.  Searches can be used to generate a library of Articles, automatically.

Once a search is performed on a topic, the site can go through everything including, "pre-processing."  

#### Project Structure for Search and Scrape

Search and Scrape functionality can be stored under src >> datacollect >> searchscrape.py, since it is inherently a server-side, static type of functionality.

```
└── src
│	  ├── datacollect
│	    ├──	init.py
│ 	  └──	searchscrape.py
│	  ├── features
│	    ├──	init.py
│ 	  └──	articletokenize.py
│	  ├── preperation
│	    ├──	init.py
│ 	  └──	knowledgebasebuild.py
│ 	├── preprocessing
│	    ├──	init.py
│ 	  └──	regexclean.py
│	  ├── evaluation
│ 	└──	js
```
#### searchscrape.py

The [Pypi for Googlesearch](https://pypi.org/project/googlesearch-python/) at the time of authoring shows version 2020.0.2, which needs to be added to our requirements.txt.

Then...

```
# import the dependencies
from googlesearch import search

# define search functionality for application
def searchterms(search_term):
    # search the given input
    search_output = search(search_term, num_results=100)
    # output as a list of URLs
    # the first item search_results[0] is the Google Search string used
    search_results = search_output[1:(num_results+1)]
    # return a list of all search results
    return(search_results)
```
For the actual scraping function, we need some different dependencies.

The [Pypi for beautifulsoup at the time of authoring](https://pypi.org/project/beautifulsoup4/) shows beautifulsoup4=4.9.3.

For finding, "any" content from any page automatically, this may be a bit trickier because pages are not necessarily structured the same way.

```
content = url_soup.find('div', {'class': 'content-area'})
```
May work better than:

```
content = url_soup.body
```

if the page in question actually has a div equivalent to 'content-area', otherwise the 'body' extraction technique may be more universal.

There are more challenges dealing with javascript heavy content, honeypots and other challenges to get more advanced which are described here:

* [Advanced Web Scraping](https://www.pluralsight.com/guides/advanced-web-scraping-tactics-python-playbook)

So in order to just bulk download all of the text, what we're going to go with for now is:

```
text = url_soup.find_all(text=True)
```
Meaning our finalized function will be:

```
def scrapeurls(search_results):
    # index search results

    # start empty list of titles and texts
    textlist = []
    titlelist = []

    # for each search result
    for counter in range(0,search_results):
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
```
Hence our regex function will do the heavy lifting further down the line.

##### Dependency Conflict - BeautifulSoup

While the most recent version of BeautifulSoup was 4.9.3, googlesearch had a conflicting dependency, based upon BeautifulSoup 4.9.1, so requirements.txt was reverted back to 4.9.1.

#### Testing Functionality in Flask Shell

Through running the flask shell, there were some problems identified:

* Need to import [requests](https://pypi.org/project/requests/) using version compatible with Google search to prevent depdendency conflict.

Running through an initial search of 100 url's, the inquiry took about 2m30s.  

There was an error or exception based upon an inability to read a certificate, which perhaps might be one of many exceptions we might find while scraping URLs.

```
aise MaxRetryError(_pool, url, error or ResponseError(cause))
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='www.photonis.com', port=443): Max retries exceeded with url: /products/mm-wave-traveling-wave-tubes (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1125)')))
```
Looking at, "len(textlist)" we still appear to have generated 92 results. What is likely needed is some kind of set of exceptions for errors, or simply a, "try" function which replaces a result with a null string for that particular column, or if we would like to structure it even further, a string which identifies the error found for that particular URL.

##### Dealing with Response Errors

try:

##### Thoughts on User Interface for Results

Users might respond well to the amount of time range it takes to generate a particular vocabulary.  If we can provide an estimate, saying that a set of 100 blogs will take 2 to 5 minutes to generate a results (really we need to take into account our entire timeline, not just the raw text collection), that might improve the user experience, giving the user a general idea of what they should expect in creating new vocabularies for various types of articles.

#### Regex Removal

Above in this post, the assumption was that raw data would be important to store - but realistically, a lot of the raw data just includes the character, '\n' - which is basically a newline character.

Within the file: src / preprocessing / regexclean.py, we can have the following:

```
import re

# compile int a regular expression object given instructions
# remove first layer of tags, characters
htmltags_re = re.compile(r'<[^>]+>')
# compile and remove newline tags
htmltags_nre = re.compile(r'\n')
# empty text tags removed list
text_tagsremovedlist = []

# removetags function
# input a list of scraped websites, output text with regex removed
def remove_tags(titlelist,textlist):

    # do this for all items in text list

    for counter in range(0,len(textlist)):
        # remove characters for a particular textlist item
        text_htmltags_removed = htmltags_re.sub('', textlist[counter])
        # remove newline function on that list item
        # append list item to text_ntags_removed list
        text_tagsremovedlist.append(htmltags_nre.sub('', text_htmltags_removed))

    return(text_tagsremovedlist)
```
[re](https://docs.python.org/3.8/library/re.html) is a python builtin module.

##### Testing Out In Flask Shell

With the above function, we get:

"TypeError: expected string or bytes-like object"

This is because type(textlist[0]) results in a <class 'bs4.element.ResultSet'> rather than a string.  However converting the result can be done simply with, "type(str(textlist[0]))"

Once this is cleared, there is still the problem of the text not being parsed properly, particularly with our very first title, wikipedia.  There are tons of irregular expressions and newlines remaining.

The following regular expression is suggested for wikipedia pages from [this stackoverflow conversation](https://stackoverflow.com/questions/4929082/python-regular-expression-with-wiki-text).

```
r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]'
```
Regex expressions within web scraping get incredibly complicated, it can be a, "data mining" exercise which as much data mining and detection of good quality data as there are sources of potential data to draw from.

To start off with, I have put some example regex files with extremely long, interspersed results within [this folder here, example_regexfiles](/example_regexfiles).

Some articles on the topic:

* [Text Data Cleaning Steps for Python](https://www.analyticsvidhya.com/blog/2014/11/text-data-cleaning-steps-python/)
* [NTALK Library for NLP Data Cleaning](https://www.analyticsvidhya.com/blog/2020/11/text-cleaning-nltk-library/)
* [HTML Data Cleaning for NLP](https://morioh.com/p/f6d2d03e6884)
* [Using NLTK](https://www.nltk.org/book/ch03.html)

So to help clean the text we could use the module, [nltk](https://pypi.org/project/nltk/) (the natural language toolkit) however this should not be confused with [ntlk](https://pypi.org/project/ntlk/) which is an empty package created by a security researcher to prevent typosquatting, since nltk is written so similarly.

##### Using NLTK

At this point it would be important to understand what GPT-2 needs in terms of inputs to be able to generate actual sentences which include a particular type of language.

According to this article [Conditional Text Generation by Fine-Tuning GPT2](https://towardsdatascience.com/conditional-text-generation-by-fine-tuning-gpt-2-11c1a9fc639d), we see that basically a few keywords are requested from the text in order to generate some kind of starter text from GPT2.

This [Colab Notebook Dealing with GPT-2 Fine-Tuning w/ Hugging Face & PyTorch](https://colab.research.google.com/drive/1g-BcoYXy-xI4yLf2jRxnaKxgM_AVrVqQ) which was originally published by [Rey Farhan](https://reyfarhan.com/posts/easy-gpt2-finetuning-huggingface/)

Within this above blog post, the author does the following:

1. Uses GPT2 with bos_token and eos_token being the startoftext and endoftext.

```
tokenizer = GPT2Tokenizer.from_pretrained('gpt2', bos_token='<|startoftext|>', eos_token='<|endoftext|>', pad_token='<|pad|>') #gpt2-medium
```
Note - there is a 768 embedding size limit for the small GPT2 model.

2. Dataset was trained with, "bios," which was literally just a bunch of written paragraph bios about various singers.  This data was fairly cleaned, presumably perfectly cleaned without HTML tags or expressions, and in sentance form to start off with.

```
dataset = GPT2Dataset(bios, tokenizer, max_length=768)
```
3. This creates a training dataset:

```
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])
```
4. Which gets put into a training dataloader.

```
train_dataloader = DataLoader(
            train_dataset,  # The training samples.
            sampler = RandomSampler(train_dataset), # Select batches randomly
            batch_size = batch_size # Trains with this batch size.
        )
```
5. Which ultimately  get enumerated out during the training process to create a model.

```
for step, batch in enumerate(train_dataloader):
```
6. This model can be used to print out generated text.

Basically, using NLTK will not be helpful unless it can really clean the text and make it into something absolutely readable and clean from the get-go.

From this [Stackoverflow Answer](https://stackoverflow.com/questions/26002076/python-nltk-clean-html-not-implemented) it appears that NLTK is no longer used for HTML cleaning as BeautifulSoup does a better job.

#### Further Pre-Built Regex Removal Functions

* [](https://gist.github.com/MrEliptik/b3f16179aa2f530781ef8ca9a16499af)
* [Cleantext Github](https://github.com/jfilter/clean-text)
* [Cleantext Pypi](https://pypi.org/project/clean-text/)

#### Removing Excess Stuff with clean-text

Utilizing the clean-text functionality:

```
def clean_text(text_tagsremovedlist):

    cleanedtags = []

    for counter in range(0,len(text_tagsremovedlist)):
        cleanedtags.append(
        clean(
            text_tagsremovedlist[counter],  # iterate over list
            fix_unicode=True,               # fix various unicode errors
            to_ascii=True,                  # transliterate to closest ASCII representation
            lower=True,                     # lowercase text
            no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
            no_urls=False,                  # replace all URLs with a special token
            no_emails=False,                # replace all email addresses with a special token
            no_phone_numbers=False,         # replace all phone numbers with a special token
            no_numbers=False,               # replace all numbers with a special token
            no_digits=False,                # replace all digits with a special token
            no_currency_symbols=False,      # replace all currency symbols with a special token
            no_punct=False,                 # remove punctuations
            replace_with_punct="",          # instead of removing punctuations you may replace them
            replace_with_url="<URL>",
            replace_with_email="<EMAIL>",
            replace_with_phone_number="<PHONE>",
            replace_with_number="<NUMBER>",
            replace_with_digit="0",
            replace_with_currency_symbol="<CUR>",
            lang="en"                        # set to 'de' for German special handling
            )
            )

    return()
```

Outputs: "Since the GPL-licensed package `unidecode` is not installed, using Python's `unicodedata` package which yields worse results."

[Unidecode](https://pypi.org/project/Unidecode/)

#### Going Back and Searching Only Visible Text from WebPages

* [BeautifulSoup - Grab Visible Webpage Text](https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text)

Basically, grabbing the visible text of a page has much better results. Of course the results are still not fully consistent, hinting at the need for a fully-customizeable vocabulary builder and editor with the capability for an editor or vocabulary builder role to be able to go in and eliminate parts of input articles, or even eliminate entire articles based upon instructions from a sponsor, to help create higher quality articles.

#### Post Search - Tokenization

Once pre-processing is finished, the articles within a group of pre-processed articles can be, "tokenized" to create a vocabulary.  This vocabulary then shows up on a list for the sponsor/user to view.

#### Post Tokenization - Knowledgebase Association

A vocabulary can automatically be assigned a name, as well as a KnowledgeBase with a name, and the vocabulary can automatically show up within that new knowledgebase.

The vocabulary can be combined with other vocabularies by adding them to the knowledgebase.

#### Post KnowledgeBase Association - Article Generation

The vocabulary can be used to generate an a long-form article, of pre-designated length, which becomes an, "autodoc."

The process of creating the autodoc involves taking a given knowledgebase and using it to fine-tune the autodoc, and hitting, "generate."  Essentially, it's a user interface and user experience wrapper for the language model generation application.

We can start out with a standard article length to generate, to ensure that articles don't become too long and overwhealm the system.

### Raw Article Library Interface

[Taking inspiration from this Dribble Design](https://dribbble.com/shots/5897384-Document-Management-System/attachments/5897384?mode=media) a stark document management system which includes a list of documents within a vocabulary, and a way to delete or add documents, or copy and paste sets of documents over to another vocabulary would likely be helpful.

![Article Interface](/readme_img/article-interface.png)

Having the ability to scan the original (perhaps both regex cleaned and non-regex cleaned to search for discrepencies) article may be helpful as well.

### Adding Ad-Hoc Articles

There should also be functionality to add ad-hoc articles to an article collection, basically adding in URL's one by one through a form rather than through a search.

### Tagging

There should also be, "tagging" capability for later perpendicular search and retrieval.

## Storing Data

### articlemodels.py

We create a class to store the articlemodels as discussed above.

Within the articlemodels.py in order to work, we import:

```
"""Database models."""
from project import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
```
For the actual model itself, there should be limitations on the amount of characters which can be held in, "raw text" and "regex removed" as there is an actual input limit to GPT2.

```
rawtext = db.Column(
		db.String(1000),
		unique=False,
		nullable=True
)
regexremoved = db.Column(
		db.String(1000),
		unique=False,
		nullable=True
)
```
The backreference should be many-to-many, relating to vocabularies via collections

```
"""backreferences Vocabulary class on collections table"""
vocabularies = relationship(
		'Collection',
		back_populates='article'
		)
```
### vocabmodels.py

The same techniques as above are used to create the models, and an association table.

### knowledgemodels.py

The same techniques as above are used to create the models, and an association table.

Note that a backreference must also be added to the "User" class to link everyhthing together:

```
"""backreferences User class on holdings table"""
knowledgebases = relationship(
		'Holding',
		back_populates='user'
		)
```
### Adding Models to App Registration

Under the app context within init.py, import via:

```
# import article models - Article and Collection
from project.static.data.rawdata import articlemodels
# import vocab models - Vocabulary and Glossary
from project.static.data.processeddata import vocabmodels
# import knowledgebase models - Knowledgebase and Holding
from project.static.data.processeddata import knowledgebasemodels

```
Performing the above gives a circular import error:

```
flask  | ImportError: cannot import name 'Article' from partially initialized module 'project.static.data.rawdata.articlemodels' (most likely due to a circular import) (/usr/src/theapp/project/static/data/rawdata/articlemodels.py)
flask exited with code 1
```
This was evidently from importing other models (classes) within each model file - for example, importing Vocabulary within the articlemodels.py file, which may not be necessary, but creates a circular import loop.  It appears that all models are imported into the application as a whole in parallel, and so there is no need to re-import them in to each other's model file.

#### Multiple Classes found Path for Revision Error

```
flask  |   File "manage.py", line 50, in <module>

...

flask  | sqlalchemy.exc.InvalidRequestError: Multiple classes found for path "Revision" in the registry of this declarative base. Please use a fully module-qualified path.

```

This was because we had incorrectly named our Glossary class, "Revision" from a copy and paste error. Fixing it yields:

```
"""Association Object - Knowledgebase Glossary(glossaries) of Vocabularies"""
class Glossary(db.Model):
    """Model for which knowledgebase retains which vocabularies"""
    """Associate database."""
    __tablename__ = 'glossaries'
```

#### Knowledgebase and Collection Relationship

```
flask  | sqlalchemy.exc.InvalidRequestError: When initializing mapper mapped class Collection->collections, expression 'Knowledgebase' failed to locate a name ('Knowledgebase'). If this is a class name, consider adding this relationship() to the <class 'project.static.data.rawdata.articlemodels.Collection'> class after both dependent classes have been defined.
```
Basically, this was because the backreferences to articles and vocabularies were wrong on the collections tables.

```
"""backreferences to article and vocabulary tables"""
vocabulary = db.relationship(
		'Vocabulary',
		back_populates='articles'
		)

article = db.relationship(
		'Article',
		back_populates='vocabularies'
		)
```

#### Vocabulary Registration

```
flask  | sqlalchemy.exc.InvalidRequestError: Multiple classes found for path "Vocabulary" in the registry of this declarative base. Please use a fully module-qualified path.
```

This may have been from the Article class, where I had placed a back-population to 'vocabulary' rather than, 'vocabularies,' the table.

```
"""backreferences Article class on collections table"""
articles = relationship(
		'Collection',
		back_populates='vocabularies'
		)
```
Changing this did nothing.

The reason actually appears to be that we do have two Vocabulary classes built, in both, "knowledgebasemodels.py" as well as, "vocabmodels.py" - the knowledgebasemodels.py class should have been the, 'Knowledgebase' class.

Once this was corrected, the error cleared.

#### class Collection has no property 'vocabularies'

```
flask  | sqlalchemy.exc.InvalidRequestError: Mapper 'mapped class Collection->collections' has no property 'vocabularies'
```

##### Backreferences on an Association Table

The proper way to do backrferences on an association table is as follows:

```
"""backreferences to itemA and itemB tables"""
itemA = db.relationship(
		'ItemA',
		back_populates='itemBs'
		)

itemB = db.relationship(
		'ItemB',
		back_populates='itemAs'
		)
```
What's happening above is that the association table is creating a new object itemA which does:

* calls on already existing Class ItemA, backpopulating to already existing table itemBs

...and the same for a new object itemB, thereby pointing to both tables and backpopulating to each other.

In the above case, there is no property, "vocabularies" because we have not imported the module 'vocabmodels.py', which we can't because it creates a circular dependency.  The solution is to initiate each model in order within the init file, working, "down the tree" in a way that allows each subsequent Class to be imported after a given model has already been started/initiated within the main __init__.py file.

![](/readme_img/initializationorder.png)

Therefore within __init__.py, the initialization order should go:

```
# import users and documents model class
# initialize in order to prevent circular dependency
from . import models
# import autodocs and revisions model class
from project.static.data.processeddata import autodocsmodels
# import knowledgebase models - Knowledgebase and Holding
from project.static.data.processeddata import knowledgebasemodels
# import vocab models - Vocabulary and Glossary
from project.static.data.processeddata import vocabmodels
# import article models - Article and Collection
from project.static.data.rawdata import articlemodels
```

And then, we shouldn't have to import anything, as everything is being created and built in order within the database.

##### Backreferences on an Target Table

So tarting out with knowledgebases, we get an error:

```
flask  | sqlalchemy.exc.InvalidRequestError: Mapper 'mapped class Knowledgebase->knowledgebases' has no property 'users'
```

This appears to be because, the proper way to set up a many-to-many backreference on a non-associaton table Class on a target table (e.g. association table relation pointing *to* the table) is as follows:

```
"""backreferences User class on Association Class"""
tableFreferences = relationship(
		'AssociationClass',
		back_populates='objectD'
		)
```
* The above backreference takes place within a Class for a table for, "objectD," basically taking place within the "ObjectD" Class.
* In the above, "tableFreferences" refers to tableF, which is the, "other" table on the opposite side of the AssociationClass table.
* AssociationClass is the name of the AssociationClass for the association table.
* objectD is backpopulated to, since it is the target object/table.

For our users class, this looked like the following:

```
"""backreferences User class on retentions table"""
documents = relationship(
		'Retention',
		back_populates='user'
		)
```

There should be two of these references for each of the following tables:

* users, which is pointed to by Holdings and Retentions
* documents which is poitned to by Retentions and Revisions
* knowledgebases which is pointed to by Holdings and Glossaries
* vocabuliaries which is pointed to by Glossaries and Collections


```
"""backreferences Knowledgbase class on glossaries table"""
vocabularies = relationship(
		'Glossary',
		back_populates='knowledgebase'
		)

"""backreferences Knowledgbase class on holdings table"""
users = relationship(
		'Holding',
		back_populates='knowledgebase'
		)

```
Moving down the line, different errors can be corrected to perfect that database relationships using the above standard naming scheme.  The main important standard is to udnerstand if you are using backreferences on an associaton table or target table.

Once all of the proper relationships have been built, the table should fully work.

#### Checking in Postgres Shell

All of the expected relations are present within postgres.

```
List of relations
Schema |      Name      | Type  |      Owner       
--------+----------------+-------+------------------
public | articles       | table | userlevels_flask
public | autodocs       | table | userlevels_flask
public | collections    | table | userlevels_flask
public | documents      | table | userlevels_flask
public | glossaries     | table | userlevels_flask
public | holdings       | table | userlevels_flask
public | knowledgebases | table | userlevels_flask
public | retentions     | table | userlevels_flask
public | revisions      | table | userlevels_flask
public | users          | table | userlevels_flask
public | vocabularies   | table | userlevels_flask
```
Investigating the new relationship tables:

```
articles

id | articlename | tags | originalurl | rawtext | regexremoved | timescraped | timepublished | created_on
----+-------------+------+-------------+---------+--------------+-------------+---------------+------------

collections

id | vocabulary_id | article_id
----+---------------+------------

glossaries

id | knowledgebase_id | vocabulary_id
----+------------------+---------------

holdings

id | knowledgebase_id | user_id
----+------------------+---------

knowledgebases

id | knowledgebasename | tags
----+-------------------+------

vocabularies

id | vocabularyname | tags | tokenizedwords | created_on
----+----------------+------+----------------+------------

```
The above tables all have the expected columns.


### Adding to Environment to Access in Shell

Adding to the shell context processor, which originally had:

```
# python shell context processor
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Document': Document, 'Retention': Retention, 'Autodoc': Autodoc,'Revision': Revision}

```
We transform this into:

```
# python shell context processor
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Document': Document, 'Retention': Retention, 'Autodoc': Autodoc,'Revision': Revision,'Holding': Holding,'Knowledgebase': Knowledgebase,'Glossary':Glossary,'Vocabulary':Vocabulary,'Collection':Collection,'Article':Article}

```

## Building Out User Functionality

### Overall Functionality Review

With the database ready to go, now it's time to build out user functionality.

Within the repo [userlevelmodelsflask](https://github.com/pwdel/userlevelmodelsflask#creating-the-forms) Balsamiq was used to model out different pages and show how functionality would look.

Fundamentally, it would be best to keep the interface and codebase as simple as possible.  To start off with, the Sponsor Dashboard can link off to a couple different interfaces:

* Knowledgebase Generator
* Autodoc Generator

The knowledgebase generator is basically a generator of a base of knowledge from which autodocs can be created.  This is knowledge a user, "puts into a computer" to help generate future articles.

An autodoc generator actually physically generates articles based upon pre-created knowledgebases.

Part of the purpose of this bifurcation is to help teach users that there is a need to use quality knowledge when building an Autodoc, you can't necessarily just say, "do it," and expect quality output, there is some layering of collection and tagging that has to happen to meet the user's specification.

While there are article generators that generate based off of a simple search term, this is one less level of abstraction from a simple search term - to ask the user to get engaged in collecting base data prior to outputting the articles.

Hypothetically we could create an, "all in one" button as well that does both the article collection as well as the document generation.

Links to these interfaces can be placed here:

![](/readme_img/sponsordashboard.png)

Within the knowledgebase menu or dashboard, there could simply be links to individual knowledgebases.  There should also be the capability to create a, "blank knowledgebase."

![](/readme_img/knowledgebasedashboard.png)

Clicking in on each individual knowledgebase should show the following - a knowledgebase is a collection of vocabularies, so links to individual vocabularies should be shown.

![](/readme_img/knowledgebaselist.png)

Vocabularies themselves are also lists - albeit they are lists of pre-processed articles.  When clicking on a vocabulary, the user should have the option to view the entire vocabulary as a printed out, "receipt" and to also go in and inspect individual articles by origin title or origin URL.

Below shows a way of looking at each individual article (link to view printed out, "receipt" view not included).  Here gives the capability to look at all individual articles included within a vocabulary.

~[](/readme_img/vocablist.png)

We can later write optional logic which further cleans up a vocabulary by making certain lines, "inactive," due to not sufficient or irregularly scraped data.

Ultimately, it's likely that the better job the program can do automatically cleaning and tagging the data, the more value the application may have overall, since on the other hand it's sort of a, "wrapper" for existing machine learning platforms.

### Simplifying To Capture Articles

The above layout is quite complicated. What might work to start off with, is to simply create the first page, a "search field," which helps a user create a knowledgebase, and then allow the knowledgebase to cascade and create an empty vocabulary, and further cascade and create an article collection.

To start off with, there would not necessarily be a need to show each level on the user dashboard, or even a success message showing that the articles were successfully built or created.

All of the data can be inspected manually via the database to start off with.

#### Route and JinjaTemplate

* The Jinjatemplate we create is the simplified form as described above, merely a searchbar.
* knowledgebase_dashboard_sponsor.jinja2
* The route goes under, "routes.py" within the sponsor routes.

The route will call several functions within our machine learning architecture, writing to each appropriate field in the database respectively, including the association tables and then redirect to a success page.

Ultimately the knowledgebase will be tied to the user through the Holding table, so that when we do show the user which knowledgebase they have access to, the Holding table will index that and display to them.

The form within the Jinjatemplate is called on as follows:

```
<div class="form-wrapper">

	<form method="POST" action="">
		{{ form.csrf_token }}
		{{ form.name }}

		<div class="search-bar">
			<fieldset class="search">
				{{ form.search.label }}
				{{ form.search(placeholder='Enter topic search here...') }}
				{% if form.search.errors %}
					<ul class="errors">
						{% for error in form.search.errors %}
							<li>{{ error }}</li>{% endfor %}
					</ul>
				{% endif %}
			</fieldset>
		</div>

		<p></p>

		<div class="submit-button">
			{{ form.submit }}
		</div>

		<p></p>

	</form>

</div>

```

##### knowledgebasegenerator() Route

* Create a route at "generator" for sponsors and decorate it with permissions.

```
from .forms import DocumentForm, SearchForm
...

@sponsor_bp.route('/sponsor/generator', methods=['GET','POST'])
@login_required
@sponsor_permission.require(http_exception=403)
@approved_permission.require(http_exception=403)
def knowledgebasegenerator_sponsor():
    # search form
    form = SearchForm()

    if form.validate_on_submit():
        # take search term from form
        # create search_string object, which is a regular object not a class
        searchstring = form.search_string.data
        # this object, "searchstring" then gets passed to another function
        # the, "googlesearch" function, located in the project structure
        # googlesearch(searchstring)
        # redirect to dashboard after search performed
        return redirect(url_for('sponsor_bp.dashboard_sponsor'))

    return render_template(
        'knowledgebase_dashboard_sponsor.jinja2',
        template='layout',
        form=form
    )

```
Of course after the <search function goes here> function is completed, there are several other strings of functions which must occur.

1. googlesearch(searchstring)
2. save results in raw article database
3. regex function, then save those results in regexcleaned database
4. vocabtokenizer, then save those results in vocab database
5. put vocab in location in knowledgebase, create name for each

These above functions can each be placed in seperate folders on the /src area of the app, since they are more server-side, non-user interface type functions.

##### Form

As shown in previous routes built within this application, the form works with, "validate on submit."

However, we have to create a new form, a "SearchForm()" which basically takes one search term as an entry.  The form has to be imported.

within forms.py, we create:

```
class SearchForm(FlaskForm):
    """Search Term input Form"""
    search_string = StringField(
        'Search',
        validators=[Optional()]
    )
    submit = SubmitField('Submit')
```

##### Linking to knowledgebasegenerator() Route from Dashboard

The following link is added on the Sponsor Dashboard jinja template:

```
<div>
	</div>
		<a href="{{ url_for('sponsor_bp.knowledgebasegenerator_sponsor') }}">Create a Knowledgbase</a>
	</div>
</div>

```

### sponsor_bp.searchsuccess_sponsor Route

This is a route that can be used for a redirect to a success message. Starting out, the user can be redirected to the sponsor dashboard.

### searchstring.py Import Functions and Usage

Within > static/src/datacollect there is already a searchscrape.py file, with the following functions:

* searchterms(search_term), outputs search_results
* scrapeurls(search_results) outputs titlelist,textlist

The outputs are:

* search_results is a dictionary list of URLs.
* titlelist and textlist are dictionary lists of strings including the raw scraped title and raw scraped text from the webpages in question.

To use the above functions from the knowledgebasegenerator() Route, we have to import the module at the top:

```
# import search functionality module
from project.static.src.datacollect.searchscrape import searchterms, scrapeurls
...
```

Upon calling the searchterms function setting 10 results, we get:

```
flask  | Sent:  ['https://www.macrumors.com/guide/mmwave-vs-sub-6ghz-5g/', 'https://www.qualcomm.com/research/5g/5g-nr/mmwave', 'https://www.ericsson.com/en/reports-and-papers/further-insights/leveraging-the-potential-of-5g-millimeter-wave', 'https://www.rcrwireless.com/20210204/5g/whats-in-the-future-of-5g-millimeter-wave', 'https://www.androidauthority.com/what-is-5g-mmwave-933631/', 'http://www.profheath.org/analysis-of-millimeter-wave-systems-for-5g/', 'https://www.globenewswire.com/en/news-release/2020/12/02/2138610/0/en/Millimeter-Wave-Opens-New-Opportunities-for-5G-Networks.html', 'https://en.wikipedia.org/wiki/5G']  ...to current_app
```
And then following this up with a urlscrapes function, we get:

```
urlscrapes = scrapeurls(searchresults)

...

/static\\/images\\/wmf-hor-googpub.png"}},"datePublished":"2009-07-03T08:46:49Z","dateModified":"2021-04-28T04:28:34Z","image":"https:\\/\\/upload.wikimedia.org\\/wikipedia\\/en\\/4\\/43\\/3GPP_5G_logo.png","headline":"5th generation of cellular mobile communications"}', '\n', '(RLQ=window.RLQ||[]).push(function(){mw.config.set({"wgBackendResponseTime":180,"wgHostname":"mw1319"});});', '\n']])  ...to current_app

```
Which is basically an expected result.

### Regex Remover & Storage

Under regex cleaning, there are a few functions stored within:

/project/static/src/preprocessing/regexclean.py

Hence, importing from there within the routes.py file...

```
from project.static.src.preprocessing.regexclean import removetags, cleantext
```

Now, looking at the results of scrapeurls...

```
urlscrapes = scrapeurls(searchresults)

type(urlscrapes)
<class 'tuple'>
```
Therefore, to access the tuple is through numerical accessing:

```
>>> urlscrapes[0][0]
<title>403 Forbidden</title>
>>> urlscrapes[0][1]
<title data-rh="true" itemprop="name" lang="en">5G NR mmWave | Qualcomm</title>
```
# urlscrapes[0] = title
# urlscrapes[1] = text

After running through regexclean.removetags we get something like this:

```
We’re a crew of WordPress professionals sharing our map to WordPress success with brilliant tutorials and tips.\', \'\\n\', \' \', \'\\n\', \'\\n\', \' \', \'\\n\', \'\\n\', \'\\n\', \'\\n\', \'\\n\', \'\\n\', \'\\n\', \'\\n\', \'\\n\', \'Top Articles\', \'How to Install WordPress\', \'\\n\', \'How to Make a Website\', \'\\n\', \'How to Create a Blog\', \'\\n\', \'SiteGround vs Bluehost\', \'\\n\', \'Best Live Chat Plugins\', \'\\n\', \' \', \'\\n\', \'\\n\', \'Our Network\', \'CodeinWP\', \'\\n\', \'Optimole\', \'\\n\', \'Domain Wheel\', \'\\n\', \'ReviveSocial\', \'\\n\', \' \', \'\\n\', \'\\n\', \'Company\', \'About us\', \'\\n\', \'Newsletter\', \'\\n\', \'Contact us\', \'\\n\', \'Careers\', \'\\n\', \'Write for Us\', \'\\n\', \' \', \'\\n\', \'\\n\', \'\\n\', \'\\n\', \'\\n\', \'\\n\', \'Copyright © 2021\', \'\\n\', \'Themeisle\', \' | Powered by \', \'VertiStudio\', \'\\n\', \'\\n\', \'\\n\', \'Terms\', \'\\n\', \'Privacy Policy\', \'\\n\', \' \', \'\\n\', \'\\n\', \'\\n\', \'\\n\', \'\\n\', \'\\n\', \'\\n\', \'\\n\', \'\\n\', \'\\n\', \'X\', \'\\n\', \'\\n\', \'Most Searched Articles\', \'10 Best Free Blogging Sites to Build Your Blog for Free in 2021: Tested, Compared and Reviewed\', \'Looking for some free blog sites to help you start sharing your writing with the world? Whether you just want to share updates with your family and friends or you want to start a blog and build a broader audience, we’ve put together ten great ...\', \'How to Create and Start a WordPress Blog in 15 Minutes or Less (Step by Step)\', \'So you want to create a WordPress blog… Congratulations! WordPress is an excellent solution for how to start a blog, plus we think blogs are super awesome! Better yet – it’s also surprisingly simple to create a WordPress blog. ...\', \'The Complete Personal Blog Guide: How to Start a Personal Blog on WordPress\', \'There’s plenty of space on the internet for everybody. People love to share ideas, give shape to their thoughts, and maybe even reach a global audience. How to put yourself on the path to achieve all of that? For once, what if you start a ...\', \'\\n\', \'Handpicked Articles\', \'How to Make a WordPress Websit
```
In the above, there are still a lot of character strings, so the regex method does not seem to be doing a full job of removing everything from an article that needs to be removed.  

[This Colab Notebook](https://colab.research.google.com/drive/1BZz_NzLFf8LwueQlxijiVnCzliCAyNcC#scrollTo=IV_UAE-kOXI-) goes through some experimentation using BeautifulSoup to remove the, "text only," from a URL along with urllib.

[urllib](https://docs.python.org/3/library/urllib.html) appears to be a standard python module.

To speed up the process of testing out new cleaning functions, one URL at a time can be entered into the urlscrape function as a pre-made one-item list:

```
testurl = ['https://www.microwavejournal.com/articles/35948-uscellular-qualcomm-ericsson-and-inseego-address-digital-divide']
```
Scraping can then be done via the following on the flask shell:

```
scraped = scrapeurls(testurl)
```
However, the textfromhtml function requires a bytes object as an input, therefore:

```
# define the scrape functionality for application
def scrapeurlsbyteresult(search_results):
    # index search results

    # start empty list of titles and texts
    textlist = []
    titlelist = []

    # for each search result through the length of search_results
    for counter in range(0,len(search_results)):
        # grab each URL
        url = search_results[counter]

        # read the url response
        url_response = urllib.request.urlopen('http://www.nytimes.com/2009/12/21/us/21storm.html').read()

        # find all text, append to list
        textlist.append(url_response)

    # return the title and text
    return(textlist)
```
After the above function is created, a test can be run through:

```
scraped = scrapeurlsbyteresult(search_results)
```
Which is shown to be a list of bytes:

```
>>> type(scraped[0])
<class 'bytes'>
```

Since passing back and fourth functions based upon the previous structure using regex is a bit confusing, it might be better to just put all definitions and functions in one file and read a url piece by piece.

On the other hand, there may be value in storing the originally scraped raw HTML.

#### Temporary Fix For Dealing with HTTPErrors

For HTTP403, basically websites preventing us from scraping, we can create an exception.  

Basically, the urllib.request.urlopen(x).read() may not work if there is a forbidden url. Therefore we can use "try/except"

```
try:
   url_response = urllib.request.urlopen(url).read()
except HTTPError as err:
	if err.code == 404:
		url_response = "404 Error"
	elif err.code == 403:
		url_response = "403 Error"
	else:
		url_response = "Other Error"
```
Note above we're just using, "Other Error" to handle all other errors at this point. A full error handling function can be created in the future.

```
# take in a dictionary list of urls
def scrapeurlsbyteresult(search_results):
    # index search results

    # start empty list of titles and texts
    textlist = []

    # for each search result through the length of search_results
    for counter in range(0,len(search_results)):
        # grab each URL
        url = search_results[counter]

        # try reading the url response
				try:
				   url_response = urllib.request.urlopen(url).read()
				except HTTPError as err:
					if err.code == 404:
						url_response = "404 Error"
					elif err.code == 403:
						url_response = "403 Error"
					else:
						url_response = "Other Error"

        # find all text, append to list
        textlist.append(url_response)

    # return the title and text
    return(textlist)
```

After the above is implemented, then any 403 errors will result in the following dictionary entry:

```
>>> b[2]
'403 Error'
```
After successfully creating a bytes-result function, "scrapeurlsbyteresult(search_results):", we can clean up the rest of our functions by eliminating them from searchscrape.py and regexclean.py.

We remove:

* scrapeurls(search_results): from searchscrape.py.
* removetags(urlscrapes): from regexclean.py

And now we have a bytes object

### Checking if HTML Tags Visible

Another meta-problem we have within scraping is being able to identify certain parts of a page through html tags. A function can check whether tags are available as follows:

```
# check if htmltags are visible
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True
```

## Storing Scraped Web Data

We have four key points of data needed to start off with to make the scraped web data useful:

* articlename (title)
* originalurl
* rawtext
* regexremoved

```
id | articlename | tags | originalurl | rawtext | regexremoved | timescraped | timepublished | created_on
----+-------------+------+-------------+---------+--------------+-------------+---------------+------------
(0 rows)

```

### Article Name

The article name is something that may actually be able to be scraped from the byte object which gets produced from scrapeurlsbyteresult().  Within this byte result, there tends to be a title within the tags <title></title> - if not, we could replace that with a shortened portion of the URL or something similar.

A new function should be created to extract the title from the byte object.

The output of scrapeurlsbyteresult(search_results) is actually a list of byte objects.  For example, if we do:

```
html_byte = request.urlopen(url).read()

we get...

type(html_byte)
>> bytes
```

This list can be accessed by y[counter].  The bytes objects can be decoded with .decode('utf8').

From there, we can use bs(html, 'htmls.parser') and then soup.find('title') to extract the title, like so:

Basically, we can add the following to our textfromhtml function:

```
...

# find title
title = soup.find('title')
# append title
extractedtitles.append(title.string)

...

# return extractedtexts object
return(extractedtexts,extractedtitles)

```
However the function will now return a tuple, rather than a single object.  Hence, reading a tuple from a function will look like the following:

```
c,d = textfromhtml(b)
```
Where each item from c corresponds to each item from d.

To store each title, we need to access the database, which we can create a seperate function for within our searchscrape.py and regclean.py files, since philosophically these are merely machine learning type server functions rather than forward-facing, "application" type functions that the user interacts with.

Keeping a firewall between the functions may help with future debugging.

So, to start off with, articlename can be stored as follows:



### Storing URLs



### Storing Titles

### Storing Raw Text from Search

### Storing Regex Cleaned Text



### Threading and Displaying a Pending Process to User

https://stackoverflow.com/questions/64545872/how-to-let-a-flask-web-page-route-run-in-the-background-while-on-another-web-p

https://stackoverflow.com/questions/40622366/flask-to-execute-other-tasks-after-return-render-template

https://stackoverflow.com/questions/40989671/background-tasks-in-flask

### Tokenizer and Vocabulary Storage

Tokenization is actually a processor intensive task and should be done with a CUDA-enabled GPU version of this program.  This task will be deferred for now.

### Adding Tags

### Calculating Data Usage

## Sorting and KnowledgeBases

### Adding Vocabularies to Knowledgebases

## Reducing Various HTTP Errors

Various HTTP Errors may occur, unforseen access errors which we haven't accounted for within this repo.  There must be a concerted effort to create a structured approach for storing and tagging all collected data based upon HTTP status at the time of web scrape.

### Dealing with 403 Errors

According to [this Stackoverflow article](https://stackoverflow.com/questions/3193060/catch-specific-http-error-in-python),

```
from urllib.error import HTTPError

import urllib
from urllib.error import HTTPError
try:
   urllib.urlopen("some url")
except HTTPError as err:
   if err.code == 404:
       <whatever>
   else:
       raise


```
Building it out in a [Colab notebook](https://colab.research.google.com/drive/1AdYKLmYVuSWW7J9xxTPzKlKeOsJ2quPf#scrollTo=FW_4ZXSiQdhj) gives the following:

```
import urllib
import urllib.request
from urllib.error import HTTPError

try:
   urllib.request.urlopen(forbidden_url).read()
except HTTPError as err:
   if err.code == 404:
     print("404 Error")
   elif err.code == 403:
     print("403 Error")
   else:
       raise
```

The possible errors are defined in the [python documentation](https://docs.python.org/3/library/urllib.error.html#urllib.error.HTTPError) as being all of those defined under [RFC 2616](https://tools.ietf.org/html/rfc2616.html), under, "[Status Code Definitions](https://tools.ietf.org/html/rfc2616.html#section-10)".

Instead of merely printing an error for each status code, we should instead write the status code to the database as a pre-defined string so that we can later count or do analytics on it, as well as create exceptions to ensure these pages are not used for linguistic processing.

### Quick Fix - Reducing 403 Errors by Specifying Browser Type

Upon initial inspection of various search results, it appears that a lot of websites give a 403 error for webscrapers.

One purported way to combat this is to use [User Agents](https://stackoverflow.com/questions/13055208/httperror-http-error-403-forbidden).

Previously, by using urlopen(), we were doing that without feeding in a browser/agent.

```
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)

try:
   req = Request(forbidden_url,headers=hdr)
   url_response = urllib.request.urlopen(req).read()
except HTTPError as err:

...

```

Where basically we tell the agent that we are viewing this through Mozilla, thereby masking ourselves and purporting to be a browser, when we're really a command line from a server.

After implementing this, the amount of webpages we can reach increases from anywhere from 1.25X to 2X.

## Future Work

* [HTTP Status Code Processing](https://tools.ietf.org/html/rfc2616.html#section-10) - as discussed above.
* [Improving Google Search Starting Point with CustomSearch API](https://stackoverflow.com/questions/41032472/how-to-query-an-advanced-search-with-google-customsearch-api)
* Advanced Google Search - Pre-Search Known Domain of Quality Text Sources
* Continual Regex Improvement
* Improving Data Input at Startpoint - Custom Search, Search Service
* Improving Data Input after collection - Custom Human Editing, Tagging, Cleaning
* Read through [this](https://tools.ietf.org/html/rfc2616.html#section-10)
* Scraped Text Quality

### Scraped Text Quality

Aside from the metaquality of the text, meaning the capability to remove regex and punctuation and other non-human readable elements, there is the actual quality of the text, which may be difficult for a computer to parse in an unsupervised manner.

We could create some kind of user method of, "flagging" or highlighting or removing portions of text that seem not to be helpful within the creation of a knowledgebase.

For example, within an example scrape of 5G mmwave, we get one result which shows the following:

```
Skip to content                 Core Competence Technology Briefs Why 5G Networks Need DCSG Routers The EBOF Solution for Hyperscale Data Centers The Benefits of Programmable Switch ASICs PAM4 Signal Integrity Virtualization of CPEs Wi-Fi Certified Agile Multiband™ BLE Beacons and Location-Based Services The New World of 400 Gbps Ethernet Network Time Synchronization TIP and Accton’s Open Packet Transponder The Emergence of 5G mmWave vOLT Concepts Intel® DPDK Performance on the SAU5081I Server CORD Fundamentals with OpenStack High-Efficiency IEEE 802.11ax SD-WANs and WAN Optimization Coherent Optics for Efficiency and Capacity R&D Capabilities Design and Development Technology Supply Chain Quality Manufacturing Solutions Cloud Data Center Solution Carrier Access Solution Campus Network Solution IoT Integration Solution SD-WAN Solution Investor Relations Letter to Shareholders Corporate Governance Annual Reports Monthly Earnings Summary Announcements Annual Meeting of Stockholders Stocks and Dividend Investor Services Press Careers Benefits and Well-being Career Development Join Accton Life @ Accton CSR Corporate Sustainability Report CSR Policies Environmental Progress Communication with Stakeholders About Accton Company Brief Accton Group Document Center Contact Us Privacy Policy     Search for:          TW                  The Emergence of 5G mmWave accton_en 2021-05-06T07:35:43+00:00   Project Description
```
While upon first glance, and particularly from the computer's perspective without any formally trained model - this text appears to be, "normal human written text," it is actually a bunch of either SEO terms which may have been hidden in the text, or menu items, or both.  The actual, "text text" starts later and looks like the following:

```
The Emergence of 5G mmWave  What is mmWave Wireless? This technology brief looks at the emergence of new 5G New Radio (5G NR or just 5G) standards for mobile cellular networks and how it has the potential to deliver a complete transformation of wireless communications. The spectrum for 5G services not only covers bands below 6 GHz, including bands currently used for 4G LTE networks, but also extends into much higher frequency bands not previously considered for mobile communications. It is the use of frequency bands in the 24 GHz to 100 GHz range, known as millimeter wave (mmWave), that provide new challenges and benefits for 5G networks.  The main focus of this technology brief is the emergence of mmWave wireless as part of the 5G revolution. The available spectrum for mmWave, the supported bandwidths, and how antenna technologies work together to deliver multiple Gigabit data rates to end users are discussed. Finally, some deployment scenarios are considered where 5G mmWave networks will start to make an impact on everyday wireless communications.  The 5G mmWave Spectrum The incredible demand for wireless data bandwidth shows no sign of slowing down in the foreseeable future. At the same time, the mobile data experience for users continues to expand and develop, putting an increasing strain on network use of available wireless spectrum. With this projected growth in mind, the cellular industry looked to other frequency bands that could possibly be utilized in the development of new 5G wireless technologies. The high-frequency bands in the spectrum above 24 GHz were targeted as having the potential to support large bandwidths and high data rates, ideal for increasing the capacity of wireless networks. ...
```
This block of text, when read through is clearly a cohesive text rather than a jumble of terms.

Finally, the end of the byte object reads like a menu would once again - this reasonably should be cleaned and taken out to leave the sweat, meaty core of actual informative text rather than SEO style menus.

```
...

More about Technology and Carrier Access Virtualization of CPEs High-Efficiency Wi-Fi 6 (IEEE 802.11ax) Accton's Technology Capabilities Carrier Access Solutions from Accton More about Technology and Carrier Access Virtualization of CPEs High-Efficiency Wi-Fi 6 (IEEE 802.11ax) Accton's Technology Capabilities Carrier Access Solutions from Accton                Site Links  Press Room  Technology Briefs  About Us  Governance  Jobs  Contact Us       Latest Sales Reports    Accton Apr 2021 sales revenue report    Accton Mar 2021 sales revenue report    Accton Technology Reports Financial Result of 2020       FIND US   No.1, Creation 3rd Rd., Hsinchu Science Park, East Dist., Hsinchu City 30077, Taiwan  +886 35 770 270      Follow Us                       Copyright 2021 © Accton Technology Corporation . All Rights Reserved              Toggle Sliding Bar Area                  Latest Sales Reports    Accton Apr 2021 sales revenue report    Accton Mar 2021 sales revenue report    Accton Technology Reports Financial Result of 2020    MWC Shanghai 2021                       We use cookies to provide the best possible user experience for those who visit our website. By using this website you agree to the placement of cookies. For more details consult our privacy policy .  OK  
```

## Conclusion

# References



* [Text Data Cleaning Steps for Python](https://www.analyticsvidhya.com/blog/2014/11/text-data-cleaning-steps-python/)
* [NTALK Library for NLP Data Cleaning](https://www.analyticsvidhya.com/blog/2020/11/text-cleaning-nltk-library/)
* [HTML Data Cleaning for NLP](https://morioh.com/p/f6d2d03e6884)
* [Using NLTK](https://www.nltk.org/book/ch03.html)
* [Advanced Web Scraping](https://www.pluralsight.com/guides/advanced-web-scraping-tactics-python-playbook)
* [Data Processing](https://www.infoq.com/articles/ml-data-processing/)
* [Preprocessing vs. Munging](https://www.xenonstack.com/blog/data-preparation/)
* [Web Scraping Tutorial](https://colab.research.google.com/github/nestauk/im-tutorials/blob/3-ysi-tutorial/notebooks/Web-Scraping/Web%20Scraping%20Tutorial.ipynb#scrollTo=pM5mWsfhqDbT)
* [Performing a Google Search in Python](https://www.geeksforgeeks.org/performing-google-search-using-python-code/)
* [](https://colab.research.google.com/drive/1axiHVKtiWmqNXKo-r3MAWHxYA_k-spNC)
* [My Webscraping Notebook](https://colab.research.google.com/drive/1fuN-rt7wA4gavo-AdZR5Uzr6w41_2kEh#scrollTo=UEh6VigNt66u)
* [Beautiful Soup Notebook](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

S
