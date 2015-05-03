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
    DASHBOARD_ADMIN = os.environ.get('DASHBOARD_ADMIN')
    POSTS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
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
        os.environ.get(
            'DATABASE_URL'
            'sqlite:///' + os.path.join(basedir, 'data.sqlite')
        )


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
