from FPproject.models import db, Model


class Hall(db.Model, Model):
    hid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer,index=True)
    name = db.Column(db.String(64), nullable=False)
    screen_type = db.Column(db.String(32))
    audio_type = db.Column(db.String(32))
    seats_num = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.Integer, nullable=False, index=True)





