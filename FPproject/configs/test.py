from FPproject.configs.default import DefaultConfig
class TestConfig(DefaultConfig):
    TESTING = True
    JSON_SORT_KEYS = False  # 稍微提高性能，
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://' 
    # 生成在进程的内存里，没有文件，进程结束就没了
