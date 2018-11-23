import pytest
from unittest.mock import Mock
from riskprofiler.risk_policies import Loi, InitialRiskPolicy, NoIncomePolicy
from riskprofiler.user_data import UserData, ItemDataCollection, HouseItemData, VehicleItemData, HouseStatus
from riskprofiler.risk_scoring import RiskScoring

@pytest.fixture
def user_data():
    return UserData(
        age=29,
        gender='male',
        marital_status='single',
        dependents=0,
        income=160000,
        houses=ItemDataCollection(
            item_datas=[
                HouseItemData(0, zip_code=123, status=HouseStatus.mortgaged)
            ]
        ),
        vehicles=ItemDataCollection(
            item_datas=[
                VehicleItemData(0, make='Tesla', model='Model S', year=2015),
                VehicleItemData(1, make='Tesla', model='Model X', year=2017),
            ]
        ),
        risk_questions=[0, 0, 0]
    )

def test_initial_risk_policy(user_data):
    scoring = Mock(spec=RiskScoring)
    policy = InitialRiskPolicy()
    policy.apply(user_data, scoring)
    assert scoring.create.call_count == 4
    assert scoring.create_item.call_count == 3
    scoring.create.assert_any_call(loi=Loi.life, score=0)
    scoring.create.assert_any_call(loi=Loi.disability, score=0)
    scoring.create.assert_any_call(loi=Loi.home, multiple_items=True)
    scoring.create.assert_any_call(loi=Loi.auto, multiple_items=True)
    scoring.create_item.assert_any_call(loi=Loi.home, item=0, score=0)
    scoring.create_item.assert_any_call(loi=Loi.auto, item=0, score=0)
    scoring.create_item.assert_any_call(loi=Loi.auto, item=1, score=0)

def test_no_income_policy(user_data):
    user_data.income = 0
    scoring = Mock(spec=RiskScoring)
    policy = NoIncomePolicy()
    policy.apply(user_data, scoring)
    scoring.disable.assert_called_once_with(loi=Loi.disability)
