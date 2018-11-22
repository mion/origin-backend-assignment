import pytest
from unittest.mock import Mock
from riskprofiler.risk_policies import InitialRiskPolicy
from riskprofiler.user_data import UserData, ItemDataCollection, HouseItemData, VehicleItemData
from riskprofiler.risk_scoring import RiskScoring

@pytest.fixture
def user_data():
    return UserData(
        age=25,
        gender='male',
        marital_status='single',
        dependents=0,
        income=50000,
        houses=ItemDataCollection(),
        vehicles=ItemDataCollection(),
        risk_questions=[0, 0, 0]
    )

def test_initial_risk_policy(user_data):
    scoring_mock = Mock(spec=RiskScoring)
    policy = InitialRiskPolicy()
    policy.apply(user_data, scoring_mock)
    scoring_mock.create.assert_called()
