#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Post, Follow, FirmType, FirmTier, Firm, \
    Company, Relationship, Geo, UserType
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG', 'default'))
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    """
    Automatically import app, db, and model objects into interactive shell.
    """
    return dict(app=app, db=db, User=User, Geo=Geo, Role=Role, Follow=Follow,
                FirmType=FirmType, FirmTier=FirmTier, Firm=Firm,
                Company=Company, Relationship=Relationship, UserType=UserType)
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
    Destroy and rebuild database with fake data.
    """
    # destroy and rebuild tables
    db.reflect()
    db.drop_all()
    db.create_all()

    # insert roles as defined in model
    Role.insert_roles()

    # insert geos and usertypes as defined in model
    Geo.insert_geos()
    UserType.insert_user_types()

    # insert firm types/tiers as defined in model
    FirmType.insert_firm_types()
    FirmTier.insert_firm_tiers()

    # insert fake admin/test users
    from random import seed
    import forgery_py
    seed()
    test_user_1 = User(
        email='salim@insights.com',
        username='salimham',
        password='password',
        confirmed=True,
        name='Salim Hamed',
        location='Seattle, WA',
        about_me=forgery_py.lorem_ipsum.sentence(),
        member_since=forgery_py.date.date(True)
    )
    test_user_2 = User(
        email='bryan@insights.com',
        username='bryan',
        password='password',
        confirmed=True,
        name='Bryan Davis',
        location='Seattle, WA',
        about_me=forgery_py.lorem_ipsum.sentence(),
        member_since=forgery_py.date.date(True)
    )
    test_user_3 = User(
        email='joe@insights.com',
        username='joe',
        password='password',
        confirmed=True,
        name='Joe Smith',
        location='San Francisco, CA',
        about_me=forgery_py.lorem_ipsum.sentence(),
        member_since=forgery_py.date.date(True)
    )
    test_user_4 = User(
        email='bill@insights.com',
        username='bill',
        password='password',
        confirmed=True,
        name='Bill Gates',
        location='Bellevue, WA',
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
    db.session.add_all([test_user_1, test_user_2, test_user_3, test_user_4,
                        admin_user])
    db.session.commit()

    # insert fake user data
    User.generate_fake(60)

    # insert fake post data
    Post.generate_fake(400)

    # insert fake followers
    Follow.generate_fake(2000)

    # insert fake firms
    Firm.generate_fake(5000)

    # insert fake companies
    Company.generate_fake(10000)

    # insert fake relationships
    Relationship.generate_fake(60000)

    # print results
    inspector = db.inspect(db.engine)
    print 'The following tables were created.'
    print '-'*17
    for table in inspector.get_table_names():
        print table


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade

    # migrate database to latest revision
    upgrade()

    # create user roles
    Role.insert_roles()

    # insert geos and usertypes as defined in model
    Geo.insert_geos()
    UserType.insert_user_types()

    # insert firm types/tiers as defined in model
    FirmType.insert_firm_types()
    FirmTier.insert_firm_tiers()


if __name__ == '__main__':
    manager.run()
