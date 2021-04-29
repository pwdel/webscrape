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
│	      └── vocabmodels.py
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

#### Going Back and Searching Only Visitble Text from WebPages

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


### Tagging


## Storing Data

### Calculating Data Usage

### Building Out Data Models

### Storing Raw Text from Search

### Regex Remover & Storage

### Tokenizer and Vocabulary Storage

### Adding Tags


## Sorting and KnowledgeBases

### Adding Vocabularies to Knowledgebases



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
