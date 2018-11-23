import pytest
from riskprofiler.risk_scoring import RiskScoring, _SingleItemRiskScore, _MultipleItemRiskScore
from riskprofiler.risk_profile_calculator import RiskAversion, RiskScoreValueMapping, RiskProfileCalculator
from riskprofiler.errors import InvalidRiskScoreOperation
from riskprofiler.user_data import UserData
from riskprofiler.risk_policies import BaseRiskPolicy
from unittest.mock import Mock

@pytest.fixture
def scoring():
    return RiskScoring({
        'single': _SingleItemRiskScore(0),
        'multiple': _MultipleItemRiskScore({
            'key0': 1,
            'key1': 2,
            'key2': 3
        })
    })

def test_risk_scoring_create_single(scoring):
    scoring.create(loi='foo', score=123)
    assert isinstance(scoring['foo'], _SingleItemRiskScore)
    assert scoring['foo'].value == 123

def test_risk_scoring_create_multiple(scoring):
    scoring.create(loi='foo', multiple_items=True)
    assert isinstance(scoring['foo'], _MultipleItemRiskScore)

def test_risk_scoring_create_item(scoring):
    scoring.create_item(loi='multiple', item='key3', score=3)
    assert scoring['multiple']['key3'] == 3

def test_risk_scoring_add_single(scoring):
    scoring.add(loi='single', points=5)
    assert scoring['single'].value == 5

def test_risk_scoring_add_multiple(scoring):
    scoring.add(loi='multiple', points=3, item='key1')
    assert scoring['multiple']['key1'] == 5

def test_risk_scoring_subtract_single(scoring):
    scoring.subtract(loi='single', points=5)
    assert scoring['single'].value == -5

def test_risk_scoring_subtract_multiple(scoring):
    scoring.subtract(loi='multiple', points=5)
    assert scoring['multiple']['key0'] == -4
    assert scoring['multiple']['key1'] == -3
    assert scoring['multiple']['key2'] == -2

def test_risk_scoring_disable(scoring):
    scoring.disable(loi='multiple')
    assert 'multiple' not in scoring

def test_risk_scoring_invalid_operation(scoring):
    with pytest.raises(InvalidRiskScoreOperation):
        scoring.create_item(loi='single', item='key0', score=42)
    with pytest.raises(InvalidRiskScoreOperation):
        scoring.add(loi='single', item='key0', points=7)
    with pytest.raises(InvalidRiskScoreOperation):
        scoring.subtract(loi='single', item='key0', points=7)

def test_scoring_map_to_profile(scoring):
    mapping = RiskScoreValueMapping()
    risk_profile = scoring.as_profile(mapping)
    assert isinstance(risk_profile, dict)
    assert risk_profile['single'] == RiskAversion.adventurous
    assert risk_profile['multiple']['key0'] == RiskAversion.average
    assert risk_profile['multiple']['key1'] == RiskAversion.average
    assert risk_profile['multiple']['key2'] == RiskAversion.conservative

def test_risk_profile_calculator():
    user_data = Mock()
    scoring = Mock(spec=RiskScoring)
    policies = [
        Mock(spec=BaseRiskPolicy),
        Mock(spec=BaseRiskPolicy)
    ]
    mapping = Mock()
    calculator = RiskProfileCalculator(
        user_data=user_data,
        risk_policies=policies,
        risk_scoring=scoring,
        risk_score_value_mapping=mapping
    )
    _ = calculator.calculate()
    policies[0].apply.assert_called_once_with(user_data, scoring)
    policies[1].apply.assert_called_once_with(user_data, scoring)
    scoring.as_profile.assert_called_once_with(mapping)
