"""
data_manager.py
"""
from models import db, User, Movie


class DataManager:
    """CRUD operations for data management"""

    def create_user(self, name):
        """Create a new user in the database"""
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user


    def get_users(self):
        """Get all users in the database"""
        return User.query.all()


    def get_movies(self, user_id):
        """Get all movies in the database by specified user id"""
        return (Movie.query
                .filter_by(user_id=user_id)
                .all())


    def add_movie(self, movie_data):
        """Add a movie to the database  """
        new_movie = Movie(
            title=movie_data["title"],
            director=movie_data["director"],
            year=int(movie_data["year"]),
            poster_url=movie_data["poster_url"]
        )
        db.session.add(new_movie)
        db.session.commit()
        return new_movie
