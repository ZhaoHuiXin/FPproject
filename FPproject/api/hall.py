from flask import jsonify, request
from flask_classy import FlaskView
from FPproject.models.hall import Hall
from FPproject.models.seat import Seat
from FPproject.api import ApiView
from FPproject.extensions.validator import Validator

class HallView(ApiView):
    @Validator(hid=int)
    def seats(self):
        hid = request.args.get('hid')
        hall = Hall.get(hid)
        if not hall:
            return {'msg': 'Hall %s not found' % hid}
        hall.seats = Seat.query.filter_by(hid=hid).all()
        return hall
