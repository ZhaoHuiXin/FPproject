from flask_script import Manager, Shell, Server
from FPproject.app import create_app
from FPproject.models import db

app = create_app()
manager = Manager(app)


def _make_context():
    from FPproject.models.cinema import Cinema
    from FPproject.models.hall import Hall
    from FPproject.models.movie import Movie
    from FPproject.models.play import Play
    from FPproject.models.seat import Seat, PlaySeat
    from FPproject.models.order import Order
    from FPproject.helper.code import Code
    from FPproject.extensions.validator import Validator
    locals().update(globals())
    # print(locals())
    return dict(**locals())

manager.add_command('shell',Shell(make_context=_make_context))
manager.add_command('runserver',Server('127.0.0.1', port=5000))

@manager.command
def createdb():
    from FPproject.models.cinema import Cinema
    from FPproject.models.hall import Hall
    from FPproject.models.movie import Movie
    from FPproject.models.play import Play
    from FPproject.models.seat import Seat, PlaySeat
    from FPproject.models.order import Order
    db.create_all()

@manager.command
def dropdb():
    from FPproject.models.cinema import Cinema
    from FPproject.models.hall import Hall
    from FPproject.models.movie import Movie
    from FPproject.models.play import Play
    from FPproject.models.seat import Seat, PlaySeat
    from FPproject.models.order import Order
    db.drop_all()

@manager.command
def testdata():
    from FPproject.models.cinema import Cinema
    from FPproject.models.movie import Movie

    Cinema.create_test_data()
    Movie.create_test_data()

@manager.command
def initdb():
    dropdb()
    createdb()
    testdata()

if __name__ == '__main__':
    manager.run()






