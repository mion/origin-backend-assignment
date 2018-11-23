import pytest
from unittest.mock import Mock
from riskprofiler.risk_policies import Loi, InitialRiskPolicy, NoIncomePolicy, NoVehiclePolicy, NoHousePolicy
from riskprofiler.user_data import UserData, ItemDataCollection, HouseItemData, VehicleItemData, HouseStatus, MaritalStatus, Gender
from riskprofiler.risk_scoring import RiskScoring

@pytest.fixture
def make_user_data():
    def _make_user_data(**kwargs):
        defaults = {
            'age': 25,
            'marital_status': MaritalStatus.single,
            'dependents': 0,
            'income': 50000,
            'houses': ItemDataCollection(),
            'vehicles': ItemDataCollection(),
            'risk_questions': [0, 0, 0]
        }
        opt = {**defaults, **kwargs}
        return UserData(
            age=opt['age'],
            gender=Gender.male,
            marital_status=opt['marital_status'],
            dependents=opt['dependents'],
            income=opt['income'],
            houses=opt['houses'],
            vehicles=opt['vehicles'],
            risk_questions=opt['risk_questions']
        )
    return _make_user_data

def test_initial_risk_policy(make_user_data):
    vehicles = ItemDataCollection(
        VehicleItemData(0, make='Tesla', model='Model S', year=2015),
        VehicleItemData(1, make='Tesla', model='Model X', year=2017)
    )
    houses = ItemDataCollection(
        HouseItemData(0, zip_code=123, status=HouseStatus.mortgaged)
    )
    user_data = make_user_data(vehicles=vehicles, houses=houses)
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

def test_no_income_policy_zero(make_user_data):
    user_data = make_user_data(income=0)
    scoring = Mock(spec=RiskScoring)
    policy = NoIncomePolicy()
    policy.apply(user_data, scoring)
    scoring.disable.assert_called_once_with(loi=Loi.disability)

def test_no_income_policy_above_zero(make_user_data):
    user_data = make_user_data(income=500)
    scoring = Mock(spec=RiskScoring)
    policy = NoIncomePolicy()
    policy.apply(user_data, scoring)
    scoring.disable.assert_not_called()

def test_no_vehicle_policy_empty(make_user_data):
    user_data = make_user_data()
    scoring = Mock(spec=RiskScoring)
    policy = NoVehiclePolicy()
    policy.apply(user_data, scoring)
    scoring.disable.assert_called_once_with(loi=Loi.auto)

def test_no_vehicle_policy_not_empty(make_user_data):
    user_data = make_user_data(vehicles=ItemDataCollection(
        VehicleItemData(0, make='Tesla', model='Model S', year=2015),
    ))
    scoring = Mock(spec=RiskScoring)
    policy = NoVehiclePolicy()
    policy.apply(user_data, scoring)
    scoring.disable.assert_not_called()

def test_no_house_policy_empty(make_user_data):
    user_data = make_user_data()
    scoring = Mock(spec=RiskScoring)
    policy = NoHousePolicy()
    policy.apply(user_data, scoring)
    scoring.disable.assert_called_once_with(loi=Loi.home)

def test_no_house_policy_not_empty(make_user_data):
    user_data = make_user_data(houses=ItemDataCollection(
        HouseItemData(0, zip_code=123, status=HouseStatus.mortgaged)
    ))
    scoring = Mock(spec=RiskScoring)
    policy = NoHousePolicy()
    policy.apply(user_data, scoring)
    scoring.disable.assert_not_called()
