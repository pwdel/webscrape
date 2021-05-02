"""Database models."""
from project import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
"""Import other Models"""
from project.static.data.rawdata.articlemodels import Article, Collection

"""Vocabulary Object"""
class Vocabulary(db.Model):
    """Vocabulary model."""
    """Describes table which includes vocabularies."""

    __tablename__ = 'vocabularies'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    vocabularyname = db.Column(
        db.String(1000),
        unique=False,
        nullable=True
    )
    tags = db.Column(
        db.String(1000),
        unique=False,
        nullable=True
    )
    tokenizedwords = db.Column(
        db.String(1000),
        unique=False,
        nullable=True
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    """backreferences Article class on collections table"""
    articles = relationship(
        'Collection',
        back_populates='vocabulary'
        )



"""Association Object - Knowledgebase Glossary(glossaries) of Vocabularies"""
class Revision(db.Model):
    """Model for which knowledgebase retains which vocabularies"""
    """Associate database."""
    __tablename__ = 'glossaries'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    knowledgebase_id = db.Column(
        db.Integer,
        db.ForeignKey('knowledgebases.id'),
        primary_key=True,
        unique=False,
        nullable=True
    )

    vocabulary_id = db.Column(
        db.Integer,
        db.ForeignKey('vocabularies.id'),
        primary_key=True,
        unique=False,
        nullable=True
    )

    """backreferences to user and document tables"""
    document = db.relationship(
        'Document',
        back_populates='autodocs'
        )

    autodoc = db.relationship(
        'Autodoc',
        back_populates='documents'
        )
