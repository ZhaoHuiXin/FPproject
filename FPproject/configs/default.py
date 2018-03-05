import os

class DefaultConfig(object):
    # BASE_DIR = os.path.abspath(os.path.join('../..', os.path.dirname(__file__)))
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))  # 前面的目录上升两级

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:666666@localhost/FPproject'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True

    # 定义LOG——DIR 路径，不写死,取BASE_DIR
    LOG_DIR = os.path.join(BASE_DIR, 'logs')




