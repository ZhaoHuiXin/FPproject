from flask import current_app

from FPproject.models import db, Model


class Movie(db.Model, Model):
    mid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    language = db.Column(db.String(32))
    subtitle = db.Column(db.String(32)) # 字幕
    show_date = db.Column(db.Date)
    vision = db.Column(db.String(16))
    model = db.Column(db.String(16))
    screen_size = db.Column(db.String(16))
    introduction = db.Column(db.Text)
    status = db.Column(db.Integer, default=0, nullable=False, index=True)

    @classmethod
    def create_test_data(cls, num=10):
        for i in range(1, num + 1):
            m = Movie()
            m.mid = i
            m.sn = str(i).zfill(10)
            m.name = '电影名称%s' % i
            m.language = '英文'
            m.subtitle = '中文'
            # m.show_date =
            m.mode = '数字'
            m.vision = '2D'
            m.screen_size = 'IMAX'
            m.introduction = 'blahblah哈哈'
            m.status = 1
            db.session.add(m)
        db.session.commit()
        current_app.logger.info('movie test data done!')

