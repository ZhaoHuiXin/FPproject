import random
import math

from datetime import datetime
import time

from flask import current_app

from FPproject.models import db, Model
import faker
class Cinema(db.Model,Model):
    cid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    address = db.Column(db.String(256), nullable=False)
    halls = db.Column(db.Integer, default=0, nullable=False)
    handle_fee = db.Column(db.Integer, default=0, nullable=False)
    buy_limit = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.Integer, nullable=False, index=True)

    @classmethod
    def create_test_data(cls, cinema_num=10, hall_num=10, play_num=10):
        start_time = time.time()
        from FPproject.models.hall import Hall
        from FPproject.models.movie import Movie
        from FPproject.models.play import Play
        from FPproject.models.seat import Seat, PlaySeat
        from FPproject.models.order import Order
        f = faker.Faker('zh_CN')
        screen_type = ['普通','IMAX']
        audio_type = ['普通','杜比环绕']
        for i in range(1, cinema_num + 1):
            cinema = Cinema()
            cinema.cid = i
            cinema.name = '%s国际影城' % f.name()
            cinema.address = f.address()
            cinema.status = 1
            cinema.save()

            for n in range(1, hall_num + 1):
                hall = Hall()
                hall.cid = cinema.cid
                hall.name = '%s号厅' % n
                hall.screen_type = random.choice(screen_type)
                hall.audio_type = random.choice(audio_type)
                hall.seats_num = 25
                hall.status = 1
                hall.save()
                # 根据seats——num生成座椅记录
                seats = []
                for s in range(1, hall.seats_num + 1):
                    seat = Seat()
                    seat.cid = cinema.cid
                    seat.hid = hall.hid
                    seat.x = s % 5 or 5
                    seat.y = math.ceil(s / 5)
                    seat.row = seat.x
                    seat.column = seat.y
                    seat.seat_type = 1
                    seat.put()
                    seats.append(seat)
                Seat.commit()

                for p in range(1, play_num + 1):
                    play = Play()
                    play.cid = cinema.cid
                    play.hid = hall.hid
                    play.mid = p
                    play.start_time = datetime.now()
                    play.duration = 3600
                    play.price_type = 1
                    play.price = 7000
                    play.market_price = 5000
                    play.lowest_price = 3000
                    play.status = 1
                    play.save()

                    for seat in seats:
                        ps = PlaySeat()
                        ps.pid = play.pid
                        ps.copy(seat)
                        ps.put()
                    PlaySeat.commit()
        current_app.logger.info('creat test data done! cost %s seconds'% (time.time()-start_time))
     




