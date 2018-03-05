from flask import request
from flask_classy import route
from FPproject.api import ApiView
from FPproject.extensions.validator import Validator, multi_int, multi_complex_int
from FPproject.models.play import Play
from FPproject.helper.code import Code
from FPproject.models.seat import PlaySeat, SeatType
from FPproject.models.order import Order, OrderStatus
from datetime import datetime
# 座位
class SeatView(ApiView):
    # 功能1,生成订单，锁定座位
    @Validator(pid=int, sid=multi_int, price=int, orderno=str)
    @route('/lock/', methods=['POST'])
    def lock(self):
        pid = request.params['pid']
        sid = request.params['sid']
        price = request.params['price'] # 用以判断价格是否低于最低价格
        orderno = request.params['orderno']
        play = Play.get(pid)
        if not play:
            return Code.play_does_not_exist,request.params
        if price < play.lowest_price:
            return Code.prcice_less_than_the_lowest_price,request.params['price']  # 只传价格也可以
        locked_seats_num = PlaySeat.lock(orderno, pid, sid)  # 调用锁定功能
        if not locked_seats_num:
            return Code.seat_lock_failed, {}  # 返回锁定失败192.168.80.152

        order = Order.create(play.cid, pid, sid)
        order.seller_order_no = orderno
        order.status = OrderStatus.locked.value
        order.tickets_num = locked_seats_num
        order.save()
        return {'locked_seats_num': locked_seats_num}

    @Validator(pid=int, sid=multi_int, orderno=str)
    @route('/unlock/', methods=['POST'])
    def unlock(self):
        pid = request.params['pid']
        sid = request.params['sid']
        orderno = request.params['orderno']
        play = Play.get(pid)
        if not play:
            return Code.play_does_not_exist, request.params

        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, request.params

        unlocked_seats_num = PlaySeat.unlock(orderno, pid, sid)
        if not unlocked_seats_num:
            return Code.seat_unlock_failed,{}
        order.status = OrderStatus.unlocked.value
        order.save()
        return {'unlock_seats_num': unlocked_seats_num}

    # seats 1-200-5000,2-200-5000
    @Validator(seats=multi_complex_int, orderno=str)
    @route('/buy/', methods=['POST'])
    def buy(self):
        seats = request.params['seats']
        # print(seats)
        orderno = request.params['orderno']
        order = Order.getby_orderno(orderno)
        # print(order)
        if not order:
            return Code.order_does_not_exist, request.params
        if order.status != OrderStatus.locked.value:
            return Code.order_status_error, {'order': orderno,
                                             'status': order.status}
        # order.seller_order_no = request.params['orderno']
        order.seller_order_no = orderno
        # order.amount = order.amount or 0
        sid_list = []
        for sid, handle_fee, price in seats:
            sid_list.append(sid)
            order.amount += (handle_fee+price)
        bought_seats_num = PlaySeat.buy(orderno, order.pid, sid_list)
        if not bought_seats_num:
            return Code.seat_buy_failed, {}
        order.tickets_num = len(seats)
        order.paid_time = datetime.now()
        order.status = OrderStatus.paid.value
        order.gen_ticket_flag()  # 生成取票码
        order.save()
        return {'bought_seats_num': bought_seats_num,
                'ticket_flag': order.ticket_flag}

