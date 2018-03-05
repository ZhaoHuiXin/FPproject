import os
import logging
from logging import FileHandler, Formatter
from flask import Flask
from logging.handlers import SMTPHandler

from FPproject.models import db, JSONEncoder
from flask_classy import FlaskView


# def create_app(debug=True):
def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object('FPproject.configs.default.DefaultConfig')
    app.config.from_object(config)
    app.json_encoder = JSONEncoder
    # 用logger模块，如果不是debug模式(即生产环境下)，启动日志
    if not app.debug:
        # 调整日志输出等级为INFO
        app.logger.setLevel(logging.INFO)

        # 定义邮件
        mail_handler = SMTPHandler(
            app.config['EMAIL_HOST'],
            app.config['SERVER_EMAIL'],
            app.config['ADMINS'],
            'boss，您的FPproject项目出现错误',
            credentials=(app.config['EMAIL_HOST_USER'],
                         app.config['EMAIL_HOST_PASSWORD'])
        )
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(Formatter('''
               Message Type:   %(levelname)s
               Location:   %(pathname)s : %(lineno)d
               Module:     %(module)s
               Funtion:    %(funcName)s
               Time:       %(asctime)s
               Message:

               %(message)s
               '''))
        app.logger.addHandler(mail_handler)

        # 设置 日志所在目录                                  # 去default.config定义
        file_handler = FileHandler(os.path.join(app.config['LOG_DIR'],'app.log'))
        #　设置记录日志最低等级为INFO
        file_handler.setLevel(logging.INFO)
        # 设置日志记录的格式   # 关键字占位符，可以传一个字典
        file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s : %(message)s'))
        #　将app生成的日志输出到指定日志文件
        app.logger.addHandler(file_handler)
    db.init_app(app)
    configure_views(app)
    app.logger.info('creat success')
    # app.config.from_object(config)

    return app


def configure_views(app):
    from FPproject.api.misc import MiscView
    from FPproject.api.cinema import CinemaView
    from FPproject.api.movie import MovieView
    from FPproject.api.hall import HallView
    from FPproject.api.seat import SeatView
    from FPproject.api.order import OrderView
    from FPproject.api.play import PlayView

    for view in locals().values():
        if type(view) == type and issubclass(view, FlaskView):
            view.register(app)


# 判断是否是类：type(view) == type and