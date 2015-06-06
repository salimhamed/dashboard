from flask import jsonify, Response, render_template, request
from flask_login import login_required, current_user
from . import search
from .forms import SearchForm
from ..models import Firm, Company
import json


@search.route('/', methods=['GET', 'POST'])
@login_required
def search_app():
    query = request.args.get('query')
    firms = Firm.query.with_entities(Firm.name)\
        .filter(Firm.name.ilike('{}%'.format(query)))\
        .order_by(Firm.name.asc()).all()
    companies = Company.query.with_entities(Company.name)\
        .filter(Company.name.ilike('{}%'.format(query)))\
        .order_by(Company.name.asc()).all()
    return render_template('search/results.html', firms=firms,
                           companies=companies)


@search.route('/_ta_prefetch')
@login_required
def prefetch():
    firms = Firm.query.with_entities(Firm.name)\
        .filter(Firm.user_id == current_user.id)
    companies = Company.query.with_entities(Company.name)\
        .filter(Company.user_id == current_user.id)
    results = firms.union(companies).order_by(Firm.name.asc()).all()
    json_results = [{'name': item.name} for item in results]
    return Response(json.dumps(json_results, indent=4),
                    mimetype='application/json')


@search.route('/_ta_remote/<query>')
@login_required
def remote(query):
    firms = Firm.query.with_entities(Firm.name)\
        .filter(Firm.user_id != current_user.id)
    companies = Company.query.with_entities(Company.name)\
        .filter(Company.user_id != current_user.id)
    results = firms.union(companies)\
        .filter(Firm.name.ilike('{}%'.format(query)))\
        .order_by(Firm.name.asc()).all()
    json_results = [{'name': item.name} for item in results]
    return Response(json.dumps(json_results, indent=4),
                    mimetype='application/json')
