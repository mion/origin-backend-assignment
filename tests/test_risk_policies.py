import pytest
from unittest.mock import Mock
from riskprofiler.risk_policies import Loi, InitialRiskPolicy, NoIncomePolicy, NoVehiclePolicy, NoHousePolicy, AgePolicy, LargeIncomePolicy, MortgagedHousePolicy, DependentsPolicy, MaritalStatusPolicy, RecentVehiclePolicy, SingleHousePolicy, SingleVehiclePolicy
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

def test_age_policy_under_30(make_user_data):
    user_data = make_user_data(age=29)
    scoring = Mock(spec=RiskScoring)
    policy = AgePolicy()
    policy.apply(user_data, scoring)
    assert scoring.subtract.call_count == 4
    scoring.subtract.assert_any_call(points=2, loi=Loi.life)
    scoring.subtract.assert_any_call(points=2, loi=Loi.disability)
    scoring.subtract.assert_any_call(points=2, loi=Loi.home)
    scoring.subtract.assert_any_call(points=2, loi=Loi.auto)

def test_age_policy_under_40(make_user_data):
    user_data = make_user_data(age=30)
    scoring = Mock(spec=RiskScoring)
    policy = AgePolicy()
    policy.apply(user_data, scoring)
    assert scoring.subtract.call_count == 4
    scoring.subtract.assert_any_call(points=1, loi=Loi.life)
    scoring.subtract.assert_any_call(points=1, loi=Loi.disability)
    scoring.subtract.assert_any_call(points=1, loi=Loi.home)
    scoring.subtract.assert_any_call(points=1, loi=Loi.auto)

def test_age_policy_over_60(make_user_data):
    user_data = make_user_data(age=61)
    scoring = Mock(spec=RiskScoring)
    policy = AgePolicy()
    policy.apply(user_data, scoring)
    assert scoring.disable.call_count == 2
    scoring.disable.assert_any_call(loi=Loi.life)
    scoring.disable.assert_any_call(loi=Loi.disability)

def test_large_income_policy_above(make_user_data):
    user_data = make_user_data(income=100)
    scoring = Mock(spec=RiskScoring)
    policy = LargeIncomePolicy(large_income_thresh=99)
    policy.apply(user_data, scoring)
    assert scoring.subtract.call_count == 4
    scoring.subtract.assert_any_call(points=1, loi=Loi.life)
    scoring.subtract.assert_any_call(points=1, loi=Loi.disability)
    scoring.subtract.assert_any_call(points=1, loi=Loi.home)
    scoring.subtract.assert_any_call(points=1, loi=Loi.auto)

def test_large_income_policy_under(make_user_data):
    user_data = make_user_data(income=100)
    scoring = Mock(spec=RiskScoring)
    policy = LargeIncomePolicy(large_income_thresh=101)
    policy.apply(user_data, scoring)
    scoring.subtract.assert_not_called()

def test_mortgaged_house_policy_empty(make_user_data):
    user_data = make_user_data()
    scoring = Mock(spec=RiskScoring)
    policy = MortgagedHousePolicy()
    policy.apply(user_data, scoring)
    scoring.add.assert_not_called()

def test_mortgaged_house_policy_not_empty(make_user_data):
    user_data = make_user_data(houses=ItemDataCollection(
        HouseItemData(0, zip_code=123, status=HouseStatus.mortgaged),
        HouseItemData(1, zip_code=124, status=HouseStatus.owned),
        HouseItemData(2, zip_code=125, status=HouseStatus.mortgaged)
    ))
    scoring = Mock(spec=RiskScoring)
    policy = MortgagedHousePolicy()
    policy.apply(user_data, scoring)
    assert scoring.add.call_count == 3
    scoring.add.assert_any_call(points=1, loi=Loi.disability)
    scoring.add.assert_any_call(points=1, loi=Loi.home, item=0)
    scoring.add.assert_any_call(points=1, loi=Loi.home, item=2)

def test_dependents_policy_zero(make_user_data):
    user_data = make_user_data()
    scoring = Mock(spec=RiskScoring)
    policy = DependentsPolicy()
    policy.apply(user_data, scoring)
    scoring.add.assert_not_called()

def test_dependents_policy_above_zero(make_user_data):
    user_data = make_user_data(dependents=3)
    scoring = Mock(spec=RiskScoring)
    policy = DependentsPolicy()
    policy.apply(user_data, scoring)
    assert scoring.add.call_count == 2
    scoring.add.assert_any_call(points=1, loi=Loi.disability)
    scoring.add.assert_any_call(points=1, loi=Loi.life)
