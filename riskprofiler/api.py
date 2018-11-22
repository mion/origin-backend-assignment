from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

bp = Blueprint('api', __name__)

@bp.route('/risk_profile', methods=('GET', 'POST'))
def get_risk_profile():
    if request.method == 'POST':
        resp = {
            'status': 'created'
        }
        return jsonify(resp)
    else:
        resp = {
            'email': 'foo@bar.com'
        }
        return jsonify(resp)
