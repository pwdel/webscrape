"""Database models."""
from project import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import Models
from project.static.data.rawdata.articlemodels import Article, Collection

# build data object and write to database
def writearticle(extractedtitles,search_results,rawbytesobject,extractedtexts):
    # # with input search_results being a dictionary list of a particular length/range
    for counter in range(0,len(search_results)):
        # grab each title
        title = extractedtitles[counter]
        # grab each URL
        url = search_results[counter]
        # grab each raw text
        raw = rawbytesobject[counter]
        # grab each regex cleaned text
        cleantext = extractedtexts[counter]
        # create new Article class instance
        newarticle = Article(
            articlename=title,
            originalurl=url,
            rawtext=raw,
            regexremoved=cleantext
            )
        # add and commit new document
        db.session.add(newarticle)
        db.session.commit()
        # add reference to Collection for this particular entry
