"""
data_manager.py

Database access and management for users and movies.
"""
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import db, User, Movie


class DataManager:
    """CRUD operations for data management"""

    def create_user(self, name):
        """Create a new user in the database"""
        try:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating user '{name}': {e}")
            return None


    def get_users(self):
        """Get all users in the database"""
        return User.query.all()


    def get_user_by_id(self, user_id):
        """Get a single user by id"""
        return User.query.get(user_id)


    def get_movies(self, user_id):
        """Get all movies in the database by specified user id"""
        return (Movie.query
                .filter_by(user_id=user_id)
                .all())


    def add_movie(self, movie_data):
        """Add a movie to the database"""
        try:
            new_movie = Movie(
                title=movie_data["title"],
                director=movie_data["director"],
                year=int(movie_data["year"]),
                poster_url=movie_data["poster_url"],
                user_id=movie_data["user_id"]
            )
            db.session.add(new_movie)
            db.session.commit()
            return new_movie
        except IntegrityError as e:
            db.session.rollback()
            print(f"IntegrityError: Movie "
                  f"'{movie_data['title']}' "
                  f"for user {movie_data['user_id']} "
                  f"already exists. {e}")
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error adding movie '{movie_data['title']}': {e}")
            return None


    def update_movie(self, movie_id, new_title):
        """Update a movie by specified id in the database"""
        movie = Movie.query.get(movie_id)
        if not movie:
            print(f"Movie with id {movie_id} not found.")
            return None
        try:
            movie.title = new_title
            db.session.commit()
            return movie
        except IntegrityError as e:
            db.session.rollback()
            print(f"IntegrityError: Movie title "
                  f"'{new_title}' already exists. {e}")
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating movie id "
                  f"{movie_id}: {e}")
            return None


    def delete_movie(self, movie_id):
        """Delete a movie by id from the database"""
        movie = Movie.query.get(movie_id)
        if not Movie:
            if not movie:
                print(f"Movie with id {movie_id} not found.")
                return False
        try:
            db.session.delete(movie)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting movie id '{movie_id}': {e}")
            return None
