from . import api
from flask_login import login_required, current_user
from flask import jsonify


@api.route('/')
@login_required
def test():
    return jsonify(results=['hello', 'world', current_user.username])
