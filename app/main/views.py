from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import SearchForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        session['company'] = form.company.data
        return redirect(url_for('main.index'))
    return render_template('index.html', form=form,
                           company=session.get('company'))
