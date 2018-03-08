from flask import jsonify
from flask_classy import FlaskView
from FPproject.models.movie import Movie
from FPproject.api import ApiView


class MovieView(ApiView):
    def all(self):
       return Movie.query.all()

