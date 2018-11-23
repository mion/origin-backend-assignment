import pytest
from riskprofiler.risk_scoring import RiskScoring, _SingleItemRiskScore, _MultipleItemRiskScore
from riskprofiler.errors import InvalidRiskScoreOperation

@pytest.fixture
def scoring():
    return RiskScoring({
        'single': _SingleItemRiskScore(0),
        'multiple': _MultipleItemRiskScore({
            'key0': 0,
            'key1': 1,
            'key2': 2
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
    assert scoring['multiple']['key1'] == 4

def test_risk_scoring_subtract_single(scoring):
    scoring.subtract(loi='single', points=5)
    assert scoring['single'].value == -5

def test_risk_scoring_subtract_multiple(scoring):
    scoring.subtract(loi='multiple', points=5)
    assert scoring['multiple']['key0'] == -5
    assert scoring['multiple']['key1'] == -4
    assert scoring['multiple']['key2'] == -3

def test_risk_scoring_disable(scoring):
    scoring.disable(loi='multiple')
    assert 'multiple' not in scoring

def test_risk_scoring_invalid_operation(scoring):
    with pytest.raises(InvalidRiskScoreOperation):
        scoring.create_item(loi='single', item='baz', score=42)
