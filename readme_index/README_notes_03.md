# Getting Started Again with Storing Scraped Web Data

We have four key points of data needed to start off with to make the scraped web data useful:

    articlename (title)
    originalurl
    rawtext
    regexremoved

id | articlename | tags | originalurl | rawtext | regexremoved | timescraped | timepublished | created_on
----+-------------+------+-------------+---------+--------------+-------------+---------------+------------
(0 rows)

### The Necessity Of "rawtext"

Rawtext is not very useful other than to perhaps inspect and ensure that the scraper is not somehow missing something embedded or coded in the rawtext itself, which is unlikely. For the sake of database conservation, we'll forgo storing, "rawtext."

* articlename (title)
* originalurl
* regexremoved

#### Where in the Code the above Data is Currently Stored

```
routes.py --> scrapeurls()
```

The above is what triggers the scrapeurl action, at least in name (we have to update this function since scrapeurls is depricated).

The following function is not used, but appears to be what was intended originally to be in the routes, a way to write articles.

```
# import write article capability
from project.static.src.datastore.articlestore import writearticle
```

However, having everything in the routes is somewhat against the paradigm of keeping the machine learning code in the static folder, with the typical web code in the routes / normal flask folder.

Ideally, the hypothetical, "scrapeurls()" function should do everything behind the scenes and the,  knowledgebasegenerator_sponsor() function should simply, "start" and "end" within the route, being opaque about what goes on underneath at least within that route file.

Instead, an, "knowledgebase_orchestration()" function should be invoked which calls each subsequent rolling part of the data munging code to keep an allegorical, "firewall," between the, "web" type stuff and the, "data processing," type stuff.

```
routes.py --> scrapeurls() -> knowledgebase_orchestration() -> textfromhtml() -> articledatabaseinsert()
```
So while textfromhtml() cleans the data, articledatabaseinsert() physically inserts it into the appropriate location in the database.

Once an article is written, then knowledgebase_orchestration() could go up the chain and subsequently write and generate, automatically:

1. Collections
2. Vocabularies
3. Glossaries
4. Knowledgebases
5. Holdings

The knowledgebase and associated data structures is then presented to the user via a Holding when the entire knowledgebase_orchestration() path has finished its set of processes.

After this point, new interfaces could be built on the route which serve as buttons to control underlying ways of cleaning up Articles, tagging and labeling things, as well as cleaning up Vocabularies and associating the former with Knowledgebases.
