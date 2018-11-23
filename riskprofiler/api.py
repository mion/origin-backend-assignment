from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from http import HTTPStatus

from .risk_policies import CURRENT_RISK_POLICIES
from .serialization import UserDataDeserializer, RiskProfileSerializer
from .risk_scoring import RiskScoreValueMapping, RiskScoring, RiskProfileCalculator
from .errors import *

bp = Blueprint('api', __name__)

@bp.route('/risk_profile', methods=['GET', 'POST'])
def get_risk_profile():
    if request.method == 'POST':
        user_data_obj = request.get_json()
        if user_data_obj is None:
            abort(HTTPStatus.BAD_REQUEST)
        deserializer = UserDataDeserializer()
        try:
            user_data = deserializer.load(user_data_obj)
            mapping = RiskScoreValueMapping()
            scoring = RiskScoring()
            calculator = RiskProfileCalculator(user_data=user_data, risk_policies=CURRENT_RISK_POLICIES, risk_scoring=scoring, risk_score_value_mapping=mapping)
            risk_profile = calculator.calculate()
            serializer = RiskProfileSerializer()
            resp = serializer.to_dict(risk_profile)
            return jsonify(resp), HTTPStatus.CREATED # Let's return 201 as if it had been saved to the DB.
        except MissingKeyDeserializationError as err:
            return jsonify({'error': str(err)}), HTTPStatus.UNPROCESSABLE_ENTITY
        except WrongKeyTypeDeserializationError as err:
            return jsonify({'error': str(err)}), HTTPStatus.UNPROCESSABLE_ENTITY
    else:
        # Here we could grab the user email through the querystring,
        # and then see if there's a risk profile for that user in the DB.
        # (We would also use an ORM for the database model...)
        resp = {}
        return jsonify(resp)
