from flask import request
from FPproject.api import ApiView
from FPproject.extensions.validator import Validator
from FPproject.models.seat import PlaySeat, SeatType
from flask_classy import route
import redis
from flask import json
r = redis.Redis()
# 座位排期
# @route('/play/seats/')
# class PlayView(ApiView):
#     @Validator(pid=int)
#     def seats(self):
#         pid = request.params['pid']
#
#         return PlaySeat.query.filter(
#             PlaySeat.pid == pid,
#             PlaySeat.seat_type != SeatType.road.value).all()

@route('/play/seats/')
class PlayView(ApiView):
    @Validator(pid=int)
    def seats(self):
        pid = request.params['pid']
        key = 'play_seats_%s' % pid
        ps = r.lrange(key, 0, -1)
        if ps:
            def dd(p):
                return json.loads(p.decode('utf-8'))
            ps = list(map(dd, ps))
            print(ps)
        if not ps:
            ps = PlaySeat.query.filter(
            # return PlaySeat.query.filter(
                PlaySeat.pid == pid,
                PlaySeat.seat_type != SeatType.road.value).all()

            r.lpush(key,*[json.dumps(p) for p in ps])
        return ps