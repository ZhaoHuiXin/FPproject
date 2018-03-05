from flask import json
from FPproject.models.seat import SeatStatus
from .helper import FlaskTestCase
from FPproject.helper.code import Code

pid = 1
sid_list = [1, 2]
sid = ','.join([str(i) for i in sid_list])
price = 5000
orderno = 'test-%s-%s' % (pid, sid)


class TestApiSeat(FlaskTestCase):
    def test_seat1_lock(self):
        locked_seats_num = len(sid_list)
        rv = self.get_succ_json('/seat/lock/',
                                method='POST',
                                orderno=orderno,
                                pid=pid,
                                sid=sid,
                                price=price)
        self.assertEqual(rv['data']['locked_seats_num'], locked_seats_num)

        # 确定锁定成功，数据写入数据库 drupal......类似于PHP织梦
        print('start-----------')

        rv = self.get_succ_json('/play/seats/', pid=pid)
        print('rv2:', rv)
        succ_count = 0
        for seat in rv['data']:
            if seat['orderno'] == orderno:
                self.assertEqual(seat['status'], SeatStatus.locked.value)
                succ_count += 1
        self.assertEqual(succ_count, locked_seats_num)  # 判断锁定的座位与

        # 确定重复锁定会失败,发送一个请求，得到data中的rc与自定义的失败一致
        rv = self.get_json('/seat/lock/',
                           method='POST',
                           orderno=orderno,
                           pid=pid,
                           sid=sid,
                           price=price)
        self.assertEqual(rv['rc'], Code.seat_lock_failed.value)
