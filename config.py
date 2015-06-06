import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hard to guess string')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # enable auto commit after request
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = '[Dashboard]'
    MAIL_SENDER = 'Dashboard Admin <dashboard@example.com>'
    DASHBOARD_ADMIN = os.environ.get('DASHBOARD_ADMIN', 'admin@insights.com')
    POSTS_PER_PAGE = 5
    FOLLOWERS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfigPsql(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        os.environ.get(
            'DEV_DATABASE_URL',
            'postgresql://localhost:5432/db_dev'
        )


class DevelopmentConfigSqlite(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        os.environ.get(
            'DEV_DATABASE_URL',
            'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
        )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = \
        os.environ.get(
            'TEST_DATABASE_URL',
            'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
        )


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = \
        "postgresql+psycopg2://" + os.environ.get("PG_ADMIN", 'admin') + ":" \
        + os.environ.get("PG_PASSWORD", 'password') + "@localhost/dashboard"


config = {
    'development_sqlite': DevelopmentConfigSqlite,
    'development_psql': DevelopmentConfigPsql,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfigPsql
}
