# PRD
from FPproject.configs.default import DefaultConfig

class ProductionConfig(DefaultConfig):
    # FIRST OF ALL
    DEBUG = False
    # 提高性能，True方便查看
    JSON_SORT_KEYS = False
    JSON_PRETTYPRINT_REGULAR = False

    SQLALCHEMY_ECHO = False
    # SEND_LOGS = True
    # EMAIL_HOST = 'smtp.exmail.qq.com'
    EMAIL_HOST = 'smtp.163.com'
    # SERVER_EMAIL = 465
    # 端口
    EMAIL_PORT = 465
    EMAIL_HOST_USER = SERVER_EMAIL = DEFAULT_FORM_EMAIL = 'momentszd@163.com'
    EMAIL_HOST_PASSWORD = 'zhx521521'
    EMAIL_USE_SSL = True
    # 接收邮箱
    ADMINS = ['313193454@qq.com']
