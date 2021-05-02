"""Database models."""
from project import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
"""Import other Models"""
from project.static.data.processeddata.vocabmodels import Vocabulary

"""Articles Object"""
class Article(db.Model):
    """Autodoc model."""
    """Describes table which includes autodocs."""

    __tablename__ = 'articles'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    articlename = db.Column(
        db.String(1000),
        unique=False,
        nullable=True
    )
    tags = db.Column(
        db.String(1000),
        unique=False,
        nullable=True
    )
    originalurl = db.Column(
        db.String(1000),
        unique=False,
        nullable=True
    )
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
    timescraped = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    timepublished = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    """backreferences Vocabulary class on collections table"""
    vocabularies = relationship(
		'Collection',
		back_populates='article'
		)


"""Association Object - Collection of Articles to form Vocabulary"""
class Collection(db.Model):
    """Model for which vocabulary contains words from which articles"""
    """Associate database."""
    __tablename__ = 'collections'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    vocabulary_id = db.Column(
        db.Integer,
        db.ForeignKey('vocabularies.id'),
        primary_key=True,
        unique=False,
        nullable=True
    )

    article_id = db.Column(
        db.Integer,
        db.ForeignKey('articles.id'),
        primary_key=True,
        unique=False,
        nullable=True
    )

    """backreferences to user and document tables"""
    vocabulary = db.relationship(
        'Vocabulary',
        back_populates='knowledgebases'
        )

    article = db.relationship(
        'Knowledgebase',
        back_populates='vocabularies'
        )
