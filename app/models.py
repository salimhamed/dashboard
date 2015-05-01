from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask.ext.login import UserMixin
from . import db, login_manager


class Permission:
    """
    A specific permission task is given a bit position.  Eight tasks are
    avalible.
    """
    FOLLOW = int('00000001', 2)
    COMMENT = int('00000010', 2)
    WRITE_ARTICLES = int('00000100', 2)
    MODERATE_COMMENTS = int('00001000', 2)
    # TASK_TBD = int('00010000', 2)
    # TASK_TBD = int('00100000', 2)
    # TASK_TBD = int('01000000', 2)
    ADMINISTER = int('10000000', 2)  # 0xff


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # is this the default role
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        """
        Update or create Role permissions.
        """
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (int('11111111', 2), False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    customer_id = db.relationship('Customer', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['DASHBOARD_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        """
        Generate a JSON Web Signature token with an expiration.
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)  # commited after end of request
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    """
    Callback function required by Flask-Login that loads a User, given the
    User identifier.  Returns User object or None.
    """
    return User.query.get(int(user_id))


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(900), nullable=False, index=True)
    record_type = db.Column(db.String(20), nullable=False)
    country_code = db.Column(db.String(2))
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))
    tier = db.Column(db.String(6))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Customer {}>'.format(self.name)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(900), unique=True, index=True)
    category = db.Column(db.String(900), nullable=False)
    sub_category = db.Column(db.String(900), nullable=False)

    def __repr__(self):
        return '<Product {}>'.format(self.name)


class Promotion(db.Model):
    __tablename__ = 'promotions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    credit_name = db.Column(db.String(600), nullable=False)
    credit_value = db.Column(db.Numeric(30, 6), nullable=False)
    credit_remaining_value = db.Column(db.Numeric(30, 6), nullable=False)
    redeemed_date = db.Column(db.Date())
    expiration_date = db.Column(db.Date(), nullable=False)
    customer_id = db.Column(db.Integer(), db.ForeignKey('customers.id'))

    def __repr__(self):
        return '<Promtion {}>'.format(self.name)


def year_default(context):
    """Context-sensitive default function for periods.year."""
    dt = context.current_parameters['period']
    return dt.year


def qrt_default(context):
    """Context-sensitive default function for periods.quarter."""
    dt = context.current_parameters['period']
    return 'Q{}-{}'.format((dt.month - 1)//3 + 1, dt.year)


class Period(db.Model):
    __tablename__ = 'periods'
    period = db.Column(db.Date(), primary_key=True, index=True)
    year = db.Column(db.Integer(), default=year_default, nullable=False)
    quarter = db.Column(db.String(7), default=qrt_default, nullable=False)

    def __repr__(self):
        return '<Period {:%m-%d-%Y}>'.format(self.period)


class Spend(db.Model):
    __tablename__ = 'spend'
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.Date(), db.ForeignKey('periods.period'))
    promotion_id = db.Column(db.Integer(), db.ForeignKey('promotions.id'))
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'))
    customer_id = db.Column(db.Integer(), db.ForeignKey('customers.id'))
    spend = db.Column(db.Numeric(30, 6))

    def __repr__(self):
        repr_str = '<Spend for customer {} on {:%m-%d-%Y}>'
        return repr_str.format(self.customer_id, self.period)
