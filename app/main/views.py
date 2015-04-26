from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import SearchForm


@main.route('/', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        session['company'] = search_form.company.data
        return redirect(url_for('main.index'))
    return render_template('index.html', form=search_form,
                           company=session.get('company'))
