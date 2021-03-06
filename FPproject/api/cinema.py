from flask import jsonify, request
from flask_classy import FlaskView
from FPproject.models.hall import Hall
from FPproject.models.cinema import Cinema
from FPproject.api import ApiView
from FPproject.helper.code import Code
from FPproject.extensions.validator import Validator
from FPproject.models.play import Play
from FPproject.models.movie import Movie

class CinemaView(ApiView):

    def all(self):
        cinemas = Cinema.query.all()
        return cinemas

    @Validator(cid=int)
    def get(self):
        cid = request.params['cid']
        cinema = Cinema.query.get(cid)
        if not cinema:
            return Code.cinema_does_not_exist, request.params

        return cinema

    @Validator(cid=int)
    def halls(self):
        cid = request.params['cid']
        print(request.values['cid'])
        cinema = Cinema.get(cid)
        if not cinema:
            return Code.cinema_does_not_exist, request.args
        cinema.halls = Hall.query.filter_by(cid=cid).all()
        return cinema

    @Validator(cid=int)
    def plays(self):
        cid = request.params['cid']
        cinema = Cinema.get(cid)
        if not cinema:
            return Code.cinema_does_not_exist, request.args
        cinema.plays = Play.query.filter_by(cid=cid).all()
        for play in cinema.plays:
            play.movie = Movie.get(play.mid)
        return cinema



