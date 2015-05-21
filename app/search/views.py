from flask import jsonify, request
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


@search.route('/_typeahead')
@login_required
def typeahead():
    results = Firm.query\
        .filter(Firm.name.ilike('%{}%'.format(query)))\
        .order_by(Firm.name.asc()).all()
    json_results = [{'id': item.id, 'name': item.name} for item in results]
    return jsonify(results=json_results)
    return jsonify(results=results)


@search.route('/_typeahead/prefetch')
@login_required
def typeahead_prefetch():
    return jsonify(results=results)
