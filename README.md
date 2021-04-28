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
│ 	  └──	tokenize.py
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

Search can simply be a formfill, with some written tips on what kinds of topics to search for, and for what purpose.  Searches can be used to generate a library of Articles, automatically.

Once a search is performed on a topic, the site can go through everything including, "pre-processing."  

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

* [Data Processing](https://www.infoq.com/articles/ml-data-processing/)
* [Preprocessing vs. Munging](https://www.xenonstack.com/blog/data-preparation/)
* [Web Scraping Tutorial](https://colab.research.google.com/github/nestauk/im-tutorials/blob/3-ysi-tutorial/notebooks/Web-Scraping/Web%20Scraping%20Tutorial.ipynb#scrollTo=pM5mWsfhqDbT)
* [Performing a Google Search in Python](https://www.geeksforgeeks.org/performing-google-search-using-python-code/)
* [](https://colab.research.google.com/drive/1axiHVKtiWmqNXKo-r3MAWHxYA_k-spNC)
* [My Webscraping Notebook](https://colab.research.google.com/drive/1fuN-rt7wA4gavo-AdZR5Uzr6w41_2kEh#scrollTo=UEh6VigNt66u)
* [Beautiful Soup Notebook](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

S
