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
