"""
models.py

This file contain the data models
to create entries in the database.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Class to create user model."""
    __tablename__ = 'user'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(
        db.String(100),
        nullable=False
    )
    # Relationship to movies
    movies = db.relationship(
        'Movie',
        backref='user',
        lazy=True
    )


    def __repr__(self):
        return (f"User("
                f"user_id = {self.id},"
                f"name={self.name})")


    def __str__(self):
        return f"User("\
               f"{self.name})"



class Movie(db.Model):
    """Class to create movie model."""
    __tablename__ = 'movie'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    title = db.Column(
        db.String(200),
        nullable=False,
    )
    director = db.Column(
        db.String(200),
        nullable=False
    )
    year = db.Column(
        db.Integer,
        nullable=True
    )
    poster_url = db.Column(
        db.String(500),
        nullable=True
    )
    # Link to Movie
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    # Different users can contain the same movie in the list
    __table_args__ = (
        db.UniqueConstraint(
            "title",
            "user_id",
            name="uix_title_user"),
        )


    def __repr__(self):
        return (f"Movie("
                f"id = {self.id},"
                f"title = {self.title},"
                f"director = {self.director},"
                f"year = {self.year},"
                f"poster_url = {self.poster_url},"
                f"user_id = {self.user_id})")


    def __str__(self):
        return   (f"Movie("
                  f"title = {self.title}"
                  f",director = {self.director},"
                  f"year = {self.year}")
