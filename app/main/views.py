from flask import render_template, session, redirect, url_for, current_app
from flask.ext.login import current_user
from .. import db
from ..models import User
from ..email import send_email
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_anonymous():
        return render_template('welcome.html')
    else:
        return render_template('index.html')
