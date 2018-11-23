import pytest
from riskprofiler.errors import ItemDataKeyNotUnique
from riskprofiler.user_data import UserData, ItemData, ItemDataCollection, VehicleItemData, HouseItemData, Gender, MaritalStatus, HouseStatus

def test_user_data_query_methods():
    user_data = UserData(
        age=42,
        gender=Gender.male,
        marital_status=MaritalStatus.married,
        dependents=3,
        income=230000,
        houses=ItemDataCollection(
            HouseItemData(0, zip_code=123, status=HouseStatus.owned),
            HouseItemData(1, zip_code=124, status=HouseStatus.mortgaged),
            HouseItemData(2, zip_code=125, status=HouseStatus.owned),
            HouseItemData(3, zip_code=126, status=HouseStatus.mortgaged)
        ),
        vehicles=ItemDataCollection(
            VehicleItemData(0, make='Tesla', model='Model S', year=2015),
            VehicleItemData(1, make='Tesla', model='Model X', year=2017)
        ),
        risk_questions=[0, 1, 1]
    )

    assert user_data.base_score() == 2
    assert user_data.is_married()
    assert user_data.has_income()
    assert user_data.is_income_above(123)
    assert user_data.is_under_age(43)
    assert user_data.is_over_age(41)
    assert user_data.has_vehicles()
    assert user_data.has_houses()
    mortgaged_houses = user_data.get_mortgaged_houses()
    assert len(mortgaged_houses) == 2
    assert mortgaged_houses[0].item_key() == 1
    assert mortgaged_houses[1].item_key() == 3
    assert user_data.get_house_at(2).zip_code == 125
    assert user_data.get_vehicle_at(1).year == 2017
    assert user_data.has_mortgaged_houses()
    assert isinstance(user_data.houses(), list)
    assert isinstance(user_data.vehicles(), list)
    assert user_data.houses_count() == 4
    assert user_data.vehicles_count() == 2
    assert user_data.has_dependents()