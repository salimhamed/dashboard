from . import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    customer_id = db.relationship('Customer', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username


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
