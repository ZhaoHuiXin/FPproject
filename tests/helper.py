from unittest import TestCase # python自带测试单元
from urllib.parse import urlencode

from flask import json
import FPproject
from FPproject.configs.test import TestConfig
from FPproject.helper.code import Code


class FlaskTestCase(TestCase): # 这是自定义测试类。所有自定义测试类，只要继承这个，初始化配置就如下
    def setUp(self): #做测试前准备工作
        app = FPproject.create_app(TestConfig)  # 在tigereye的init里面
        app.logger.disabled = True # 关闭日志
        self.app = app.test_client() #app对象方法，可以方便的测试，不用起服务，它就走流程，像scrapy shell
        # 不通过http的请求就可以调用接口
        with app.app_context():
            from FPproject.models import db
            from FPproject.models.cinema import Cinema
            from FPproject.models.hall import Hall
            from FPproject.models.movie import Movie
            from FPproject.models.play import Play
            from FPproject.models.seat import Seat, PlaySeat
            from FPproject.models.order import Order
            db.create_all()
            Cinema.create_test_data(cinema_num=1, hall_num=3, play_num=3)
            Movie.create_test_data()
            # 数据最好存在内存中，避免数据库出现脏数据
            # 传200必须返回200

    def assert_get(self, uri, assertcode=200, method='GET', **params):
        if method == 'POST':
            rv = self.app.post(uri, data=params)
        else:
            if params:
                rv = self.app.get('%s?%s' % (uri, urlencode(params))) # urlencode将参数拼接成url可传递形式
            else:
                rv = self.app.get(uri)
        self.assertEqual(rv.status_code, assertcode)
        return rv

    def get200(self, uri, method='GET', **params):
        return self.assert_get(uri, 200, method, **params)

    def get_json(self, uri, method='GET', **params):
        rv = self.get200(uri, method, **params)
        return json.loads(rv.data)

    def get_succ_json(self, uri, method='GET', **params):
        data = self.get_json(uri, method, **params)
        self.assertEquals(data['rc'], Code.succ.value)
        return data
