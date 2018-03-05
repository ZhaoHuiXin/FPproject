# 方便，对外隐藏了 app的实现
from FPproject import create_app
from FPproject.configs.production import ProductionConfig
# 创建使用生产环境配置的app
application = create_app(config=ProductionConfig)
# gunicorn wsgi 默认去找application，改成别的要指定 gunicorn wsgi:xxx(app名)