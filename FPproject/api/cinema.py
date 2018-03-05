from flask import jsonify, request
from flask_classy import FlaskView
from FPproject.models.hall import Hall
from FPproject.models.cinema import Cinema
from FPproject.api import ApiView
from FPproject.helper.code import Code
from FPproject.extensions.validator import Validator
from FPproject.models.play import Play
from FPproject.models.movie import Movie
# 为了简化return jsonify。。。自定义了ApiView,它继承自FlaskView，
# 改写了其中构造response的部分，使其能对将要制造response对象的数据进行自定义格式化
class CinemaView(ApiView):

    def all(self):
        cinemas = Cinema.query.all()
        return cinemas

    # 传id返回具体详细信息
    @Validator(cid=int)
    def get(self):
        cid = request.params['cid']
        cinema = Cinema.query.get(cid)
        if not cinema:
            return Code.cinema_does_not_exist, request.params

        return cinema
    # 为了能对客户端传递的参数进行类型过滤，并返回些许提示
    # 定义了类装饰器Validator
    @Validator(cid=int)
    def halls(self):
        # cid = request.args['cid']
        cid = request.params['cid']
        print(request.values['cid'])
        cinema = Cinema.get(cid)
        if not cinema:
            # return 1, {'cid':cid}
            # return 1, request.args
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



