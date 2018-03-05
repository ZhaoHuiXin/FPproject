from flask import json
from .helper import FlaskTestCase
from FPproject.helper.code import Code


class TestApiCinema(FlaskTestCase):
    def test_cinema_all(self):
        self.get_succ_json('/cinema/all/')
        # response = self.app.get('/cinema/all/')
        # self.assertEqual(response.status_code, 200)  # 断言assert,不符合就报错
        # data = json.loads(response.data)
        # print(data)
        # self.assertEqual(data['rc'], Code.succ.value)  # 断言是否返回了成功状态码

    def test_cinema_halls(self):
        self.assert_get('/cinema/halls/',400)
        # self.get_succ_json('/cinema/all/')
        # data = self.get_succ_json('/cinema/halls/', cid=1)
        data = self.get_succ_json('/cinema/halls/', cid=1)
        self.assertIsNotNone(data['data'])
