#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

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

    # print results
    inspector = db.inspect(db.engine)
    print 'The following tables were created.'
    print '-'*17
    for table in inspector.get_table_names():
        print table


if __name__ == '__main__':
    manager.run()
