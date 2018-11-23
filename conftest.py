import os
import tempfile

import pytest
from riskprofiler import create_app


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True
    })

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def user_data_json():
    return {
        'age': 35,
        'gender': 'female',
        'marital_status': 'married',
        'dependents': 2,
        'income': 150000,
        'risk_questions': [0, 1, 0],
        'houses': [
            {'key': 0, 'zip_code': 123, 'status': 'owned'},
            {'key': 1, 'zip_code': 456, 'status': 'mortgaged'}
        ],
        'vehicles': [
            {'key': 0, 'make': 'Maker', 'model': 'Model A', 'year': 2008},
            {'key': 1, 'make': 'Maker', 'model': 'Model B', 'year': 2018}
        ]
    }