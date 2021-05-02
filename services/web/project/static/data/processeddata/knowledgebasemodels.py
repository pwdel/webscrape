"""Database models."""
from project import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
"""Import other Models"""
from project.static.data.processeddatata.vocabmodels import Vocabulary, Glossary

"""Knowledgebase Object"""
class Vocabulary(db.Model):
    """Knowledgebase model."""
    """Describes table which includes knowledgebase, which are folders of vocabularies."""

    __tablename__ = 'knowledgebases'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    knowledgebasename = db.Column(
        db.String(1000),
        unique=False,
        nullable=True
    )
    tags = db.Column(
        db.String(1000),
        unique=False,
        nullable=True
    )

    """backreferences Vocabulary class on glossaries table"""
    vocabularies = relationship(
        'Glossary',
        back_populates='knowledgebase'
        )

    """backreferences User class on holdings table"""
    user = relationship(
        'Holding',
        back_populates='knowledgebase'
        )


"""Association Object - User Holding(holding) of Knowledgebases"""
class Holding(db.Model):
    """Model for which user retains which knowledgebases"""
    """Associate database."""
    __tablename__ = 'holdings'

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

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True,
        unique=False,
        nullable=True
    )

    """backreferences to user and knowledgebase tables"""
    knowledgebase = db.relationship(
        'Knowledgebase',
        back_populates='users'
        )

    user = db.relationship(
        'User',
        back_populates='knowledgebases'
        )
