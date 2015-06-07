from . import api
from flask_login import login_required, current_user
from flask import Response
import json


@api.route('/firm_summary')
@login_required
def firm_summary():
    summary = current_user.firm_summary()
    return Response(json.dumps(summary, indent=4), mimetype='application/json')
