from flask import jsonify
from flask_login import login_required
from . import search
from ..models import Firm, Company


@search.route('/query/<query>')
@login_required
def search_app(query):
    results = Firm.query\
        .filter(Firm.name.ilike('%{}%'.format(query)))\
        .order_by(Firm.name.asc()).all()
    json_results = [{'id': item.id, 'name': item.name} for item in results]
    return jsonify(results=json_results)


@search.route('/_typeahead/<query>')
@login_required
def typeahead(query):
    firms = Firm.query.with_entities(Firm.name)
    companies = Company.query.with_entities(Company.name)
    results = firms.union(companies)\
        .filter(Firm.name.ilike('{}%'.format(query)))\
        .order_by(Firm.name.asc())\
        .limit(15).all()
    json_results = [{'name': item.name} for item in results]
    return jsonify(results=json_results)


@search.route('/_typeahead/prefetch')
@login_required
def typeahead_prefetch():
    firms = Firm.query.with_entities(Firm.name)
    companies = Company.query.with_entities(Company.name)
    results = firms.union(companies)\
        .order_by(Firm.name.asc()).all()
    json_results = [{'name': item.name} for item in results]
    return jsonify(results=json_results)
