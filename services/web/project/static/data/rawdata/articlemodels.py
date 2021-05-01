"""Database models."""
from project import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


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
