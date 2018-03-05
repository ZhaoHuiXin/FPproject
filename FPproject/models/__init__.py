from flask_sqlalchemy import SQLAlchemy
from flask import json as _json
db = SQLAlchemy()

class Model(object):
    @classmethod
    def get(cls, primary_key):
        return cls.query.get(primary_key)

    def put(self):
        db.session.add(self)

    @classmethod
    def commit(cls):
        db.session.commit()

    @classmethod
    def rollback(cls):
        db.session.rollback()

    def delete(self):
        db.session.delete(self)

    def save(self):
        try:
            self.put()
            self.commit()
        except Exception:
            self.rollback()
            raise

    def __json__(self):
        data = {}
        keys = vars(self).keys()
        for key in keys:
            if not key.startswith('_'):
                data[key] = getattr(self, key)
                # self.name
                # getattr(self, 'name')
        return data

class JSONEncoder(_json.JSONEncoder):
    def default(self, o):
        if isinstance(o, db.Model):
            return o.__json__()
        return _json.JSONEncoder.default(self, o)