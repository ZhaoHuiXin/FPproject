from random import randint
from FPproject.models import db, Model
from sqlalchemy import text
from sqlalchemy.sql import func
from FPproject.helper import tetime
from enum import Enum, unique

@unique
class OrderStatus(Enum):

    """已锁座"""
    locked = 1
    """解锁"""
    unlocked = 2
    """自动解锁(超过一定时间未操作被系统自动解锁)"""
    auto_unlocked = 3
    """已支付"""
    paid = 4
    """已出票"""
    printed = 5
    """退款"""
    refund = 6

class Order(db.Model, Model):
    __tablename__= 'orders'
    # 订单id，我们自己的订单号
    oid = db.Column(db.String(32), primary_key=True)
    # 销售方订单号
    seller_order_no = db.Column(db.String(32), index=True)
    cid = db.Column(db.Integer)
    pid = db.Column(db.Integer)
    sid = db.Column(db.String(50))
    # 取票码
    ticket_flag = db.Column(db.String(64))
    tickets_num = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    paid_time = db.Column(db.DateTime)  # 支付时间
    printed_time = db.Column(db.DateTime)  # 取票时间案
    refund_time = db.Column(db.DateTime)  # 退款时间
    created_time = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))  # 创建时间
    # 数据更新时候，将这个字段设置成当前时间
    updated_time = db.Column(db.DateTime, onupdate=func.now())  # 最后更新时间

    status = db.Column(db.Integer, default=0, nullable=False, index=True)

    # 创建订单，并且锁座
    @classmethod
    def create(cls, cid, pid, sid):
        order = cls()
        order.oid = '%s%s%s' % (tetime.now(),randint(100000, 999999), pid)
        order.cid = cid
        order.pid = pid
        # order.sid = sid
        if type(sid) == list:
            order.sid = ','.join(str(i) for i in sid)
        else:
            order.sid = sid
        return order

    @classmethod
    def getby_orderno(cls, orderno):
        return Order.query.filter_by(seller_order_no=orderno).first()

    def gen_ticket_flag(self):
        self.ticket_flag = ''.join([str(randint(1000, 9999)) for i in range(8)])

    def validate(self, ticket_flag):
        return self.ticket_flag == ticket_flag

    @classmethod
    def getby_ticket_flag(cls, ticket_flag):
        return cls.query.filter_by(ticket_flag=ticket_flag).first()
