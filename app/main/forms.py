from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class SearchForm(Form):
    company = StringField('Company Name', validators=[Required()])
    submit = SubmitField('Search')
