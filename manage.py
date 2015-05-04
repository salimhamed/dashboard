#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Post
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG', 'default'))
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    """
    Automatically import app, db, and model objects into interactive shell.
    """
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """
    Run the unit tests.
    """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def db_rebuild():
    """
    Destroy and rebuild database.
    """
    # destroy and rebuild tables
    db.drop_all()
    db.create_all()

    # insert roles as defined in model
    Role.insert_roles()

    # insert fake user data
    from random import seed
    import forgery_py
    seed()

    test_user = User(
        email='test@insights.com',
        username='testuser',
        password='password',
        confirmed=True,
        name='Joe Smith',
        location='Seattle, WA',
        about_me=forgery_py.lorem_ipsum.sentence(),
        member_since=forgery_py.date.date(True)
    )
    admin_user = User(
        email='admin@insights.com',
        username='admin',
        password='password',
        confirmed=True,
        name='Bill Gates',
        location='Seattle, WA',
        about_me=forgery_py.lorem_ipsum.sentence(),
        member_since=forgery_py.date.date(True)
    )
    db.session.add_all([test_user, admin_user])
    db.session.commit()

    # insert fake data
    User.generate_fake(200)

    # insert fake post data
    Post.generate_fake(400)

    # print results
    inspector = db.inspect(db.engine)
    print 'The following tables were created.'
    print '-'*17
    for table in inspector.get_table_names():
        print table


if __name__ == '__main__':
    manager.run()
