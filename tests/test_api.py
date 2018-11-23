import pytest
from http import HTTPStatus

@pytest.mark.parametrize(('deleted_key'), (
    ('age'), ('gender'), ('marital_status'), ('dependents'),
    ('income'), ('risk_questions'), ('houses'), ('vehicles')
))
def test_risk_profile_post_missing_key(client, user_data_json, deleted_key):
    del user_data_json[deleted_key]
    resp = client.post('/risk_profile', json=user_data_json)
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    resp_json = resp.get_json()
    assert 'error' in resp_json
    error_msg = resp_json['error']
    assert 'missing key' in error_msg
    assert deleted_key in error_msg

@pytest.mark.parametrize(('wrong_key', 'wrong_value'), (
    ('age', 23.0), ('gender', False), ('marital_status', 0), ('dependents', 2.0),
    ('income', 43000.0), ('risk_questions', {}), ('houses', {}), ('vehicles', {})
))
def test_risk_profile_post_wrong_key_type(client, user_data_json, wrong_key, wrong_value):
    user_data_json[wrong_key] = wrong_value
    resp = client.post('/risk_profile', json=user_data_json)
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    resp_json = resp.get_json()
    assert 'error' in resp_json
    error_msg = resp_json['error']
    assert 'wrong type' in error_msg
    assert wrong_key in error_msg

def test_risk_profile_post_valid_payload(client, user_data_json):
    resp = client.post('/risk_profile', json=user_data_json)
    assert resp.status_code == HTTPStatus.CREATED
    resp_json = resp.get_json()
    assert 'auto' in resp_json
    assert 'home' in resp_json
    assert 'disability' in resp_json
    assert 'life' in resp_json

def test_risk_profile_post_disabled_field_payload(client, user_data_json):
    user_data_json['age'] = 90
    resp = client.post('/risk_profile', json=user_data_json)
    assert resp.status_code == HTTPStatus.CREATED
    resp_json = resp.get_json()
    assert 'auto' in resp_json
    assert 'home' in resp_json
    assert 'disability' not in resp_json
    assert 'life' not in resp_json
