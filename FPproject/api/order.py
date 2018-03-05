from flask import request
from flask_classy import route
from FPproject.api import ApiView
from FPproject.extensions.validator import Validator, multi_int, multi_complex_int
from FPproject.models.movie import Movie
from FPproject.models.play import Play
from FPproject.helper.code import Code
from FPproject.models.seat import PlaySeat, SeatType
from FPproject.models.order import Order, OrderStatus
from datetime import datetime

class OrderView(ApiView):
    @route('/refund/', methods=['POST'])
    @Validator(orderno=str, ticket_flag=str, sid=multi_int)
    def refund_ticket(self):
        orderno = request.params['orderno']
        ticket_flag = request.params['ticket_flag']
        seats = request.params['sid']

        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist,{'orderno':orderno}
        if order.status == OrderStatus.printed.value:
            return Code.ticket_printed_already,{}

        if order.status != OrderStatus.paid.value:
            return  Code.order_not_paid_yet,{}

        # validate校验验证码方法
        if not order.validate(ticket_flag):
            return Code.ticket_flag_error,{'ticket_flag': ticket_flag}
        # refund 退款方法，改变订单的属性
        refund_num = PlaySeat.refund(orderno, order.pid, seats)
        if not refund_num:
            return Code.ticket_refund_failed,{}

        order.status = OrderStatus.refund.value
        order.refund_time = datetime.now()
        order.save()
        return {'refund_num': refund_num}

    @route('/ticket/print/', methods=['POST'])
    @Validator(orderno=str, ticket_flag=str, sid=multi_int)
    def print_ticket(self):
        orderno = request.params['orderno']
        ticket_flag = request.params['ticket_flag']
        seats = request.params['sid']

        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, {'orderno': orderno}
        if order.status == OrderStatus.printed.value:
            return Code.ticket_printed_already, {}

        if order.status != OrderStatus.paid.value:
            return Code.order_not_paid_yet, {}

        # validate校验验证码方法
        if not order.validate(ticket_flag):
            return Code.ticket_flag_error, {'ticket_flag': ticket_flag}

        printed_num = PlaySeat.print_tickets(order.seller_order_no,order.pid,seats)

        if not printed_num:
            return Code.ticket_print_failed.value,{}
        order.status = OrderStatus.printed.value
        order.printed_time = datetime.now()
        order.save()
        return {'printed_num': printed_num}

    @route('/ticket/info/')
    @Validator(orderno=str)
    def ticket_info(self):
        orderno = request.params['orderno']
        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, {'orderno': orderno}
        order.play = Play.get(order.pid)
        order.movie = Movie.get(order.play.mid)
        # 这里还要在PlaySeat中实现一个getby_orderno
        order.tickets = PlaySeat.getby_orderno(orderno)
        return order


