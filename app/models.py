import hashlib
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager


class Permission:
    """
    A specific permission task is given a bit position.  Eight tasks are
    avalible because there are eight bits in a byte.
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
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        """Update or create all Roles."""
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),  # User Role is default
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


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint

        users = User.query.all()
        # The method seed() sets the integer starting value used in generating
        # random numbers. Call this function before calling any other random
        # module function.
        seed()
        for i in range(count):
            int_follower = randint(0, len(users) - 1)
            int_followed = randint(0, len(users) - 1)
            if int_follower != int_followed:
                f = Follow(
                    follower=users[int_follower],
                    followed=users[int_followed]
                )
                db.session.add(f)
                # relationship might not be random, in which case rollback
                try:
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())

    # 'default' can take a function so each time a default value needs to be
    # produced, the function is called
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',   # return query, not items
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',  # return query, not items
                                cascade='all, delete-orphan')
    firms = db.relationship('Firm', backref='owner', lazy='dynamic')
    companies = db.relationship('Company', backref='owner', lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        # The method seed() sets the integer starting value used in generating
        # random numbers. Call this function before calling any other random
        # module function.
        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     confirmed=True,
                     name=forgery_py.name.full_name(),
                     location=forgery_py.address.city(),
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True))
            db.session.add(u)
            # user might not be random, in which case rollback
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['DASHBOARD_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

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
        self.avatar_hash = hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar(self, size=100, default='identicon', rating='g'):
        # match the security of the client request
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'

        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False
# Register AnonymousUser as the class assigned to 'current_user' when the user
# is not logged in.  This will enable the app to call 'current_user.can()'
# without having to first check if the user is logged in
login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    """
    Callback function required by Flask-Login that loads a User, given the
    User identifier.  Returns User object or None.
    """
    return User.query.get(int(user_id))


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        # The method seed() sets the integer starting value used in generating
        # random numbers. Call this function before calling any other random
        # module function.
        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Post(body=forgery_py.lorem_ipsum.paragraphs(randint(5, 15)),
                     timestamp=forgery_py.date.date(True),
                     author=u)
            db.session.add(p)
            db.session.commit()


class Relationship(db.Model):
    __tablename__ = 'relationships'
    firm_id = db.Column(db.Integer, db.ForeignKey('firms.id'),
                        primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'),
                           primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint

        firm_offset = Firm.query.count() - 1
        company_offset = Company.query.count() - 1
        seed()
        for i in range(count):
            f = Firm.query.offset(randint(0, firm_offset)).first()
            c = Company.query.offset(randint(0, company_offset)).first()
            rel = Relationship(firms=f, companies=c)
            db.session.add(rel)
            # relationship might already exist, then rollback
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


class FirmType(db.Model):
    __tablename__ = 'firm_types'
    id = db.Column(db.Integer, primary_key=True)
    firm_type = db.Column(db.String(64), unique=True)
    firms = db.relationship('Firm', backref='type', lazy='dynamic')

    @staticmethod
    def insert_firm_types():
        """Update or create all Firm Types"""
        types = ['Venture Capital',
                 'Accelerator/Incubator',
                 'Startup Organization']
        for t in types:
            firm_type = FirmType.query.filter_by(firm_type=t).first()
            if firm_type is None:
                firm_type = FirmType(firm_type=t)
            db.session.add(firm_type)
        db.session.commit()

    def __repr__(self):
        return '<FirmType %r>' % self.firm_type


class FirmTier(db.Model):
    __tablename__ = 'firm_tiers'
    id = db.Column(db.Integer, primary_key=True)
    firm_tier = db.Column(db.String(64), unique=True)
    firms = db.relationship('Firm', backref='tier', lazy='dynamic')

    @staticmethod
    def insert_firm_tiers():
        """Update or create all Firm Tiers"""
        tiers = ['Tier 1',
                 'Tier 2',
                 'Tier 3']
        for t in tiers:
            firm_tier = FirmTier.query.filter_by(firm_tier=t).first()
            if firm_tier is None:
                firm_tier = FirmTier(firm_tier=t)
            db.session.add(firm_tier)
        db.session.commit()

    def __repr__(self):
        return '<FirmTier %r>' % self.firm_tier


class Firm(db.Model):
    __tablename__ = 'firms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(900), nullable=False, index=True)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    firm_type_id = db.Column(db.Integer, db.ForeignKey('firm_types.id'))
    firm_tier_id = db.Column(db.Integer, db.ForeignKey('firm_tiers.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    companies = db.relationship('Relationship',
                                foreign_keys=[Relationship.firm_id],
                                backref=db.backref('firms', lazy='joined'),
                                lazy='dynamic',  # return query, not items
                                cascade='all, delete-orphan')

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        type_count = FirmType.query.count()
        tier_count = FirmTier.query.count()
        for i in range(count):
            # create fake relationships
            tp = FirmType.query.offset(randint(0, type_count - 1)).first()
            tr = FirmTier.query.offset(randint(0, tier_count - 1)).first()
            u = User.query.offset(randint(0, user_count - 1)).first()

            # create fake firm
            f = Firm(name=forgery_py.name.company_name(),
                     city=forgery_py.address.city(),
                     state=forgery_py.address.state_abbrev(),
                     country=forgery_py.address.country(),
                     type=tp,
                     tier=tr,
                     owner=u,)
            db.session.add(f)
            # custome might not be random, in which case rollback
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<Firm {}>'.format(self.name)


class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(900), nullable=False, index=True)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    firms = db.relationship('Relationship',
                            foreign_keys=[Relationship.company_id],
                            backref=db.backref('companies', lazy='joined'),
                            lazy='dynamic',   # return query, not items
                            cascade='all, delete-orphan')

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py

        seed()
        user_offset = User.query.count() - 1
        for i in range(count):
            # create fake relationships
            u = User.query.offset(randint(0, user_offset)).first()

            # create fake company
            c = Company(name=forgery_py.name.company_name(),
                        city=forgery_py.address.city(),
                        state=forgery_py.address.state_abbrev(),
                        country=forgery_py.address.country(),
                        owner=u)
            db.session.add(c)
            # company might not be random, in which case rollback
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<Company {}>'.format(self.name)
