from flask import current_app, request
from flask_classy import route, FlaskView


class MiscView(FlaskView):

    def index(self):
        return self.check()

    def check(self):
        current_app.logger.info('check from %s' % request.remote_addr)
        return 'I am OK'
    def error(self):
        1 / 0
