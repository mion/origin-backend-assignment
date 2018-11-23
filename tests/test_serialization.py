import pytest
from riskprofiler.user_data import UserData, ItemData, ItemDataCollection, VehicleItemData, HouseItemData, Gender, MaritalStatus, HouseStatus
from riskprofiler.serialization import UserDataDeserializer, HouseItemDataDeserializer, VehicleItemDataDeserializer

@pytest.fixture
def user_data_obj():
    return {
        'age': 35,
        'gender': 'female',
        'marital_status': 'married',
        'dependents': 2,
        'income': 150000,
        'risk_questions': [0, 0, 0],
        'houses': [
            {'key': 0, 'zip_code': 123, 'status': 'owned'},
            {'key': 1, 'zip_code': 456, 'status': 'mortgaged'}
        ],
        'vehicles': [
            {'key': 0, 'make': 'Maker', 'model': 'Model A', 'year': 2008},
            {'key': 1, 'make': 'Maker', 'model': 'Model B', 'year': 2018}
        ]
    }

def test_user_data_deserialization(user_data_obj):
    deserializer = UserDataDeserializer()
    user_data = deserializer.load(user_data_obj)
    assert isinstance(user_data, UserData)
    assert user_data.age == 35
    assert isinstance(user_data.gender, Gender)
    assert user_data.gender == Gender.female
    assert isinstance(user_data.marital_status, MaritalStatus)
    assert user_data.marital_status == MaritalStatus.married
    assert user_data.dependents == 2
    assert user_data.income == 150000
    assert user_data.risk_questions == [0, 0, 0]
    assert isinstance(user_data.house_collec, ItemDataCollection)
    assert len(user_data.house_collec) == 2
    assert isinstance(user_data.vehicle_collec, ItemDataCollection)
    assert len(user_data.vehicle_collec) == 2

def test_house_item_data_deserialization():
    deserializer = HouseItemDataDeserializer()
    house_item_data = deserializer.load({
        'key': 7,
        'zip_code': 987,
        'status': 'mortgaged'
    })
    assert isinstance(house_item_data, HouseItemData)
    assert house_item_data.item_key() == 7
    assert house_item_data.zip_code == 987
    assert house_item_data.status == HouseStatus.mortgaged

def test_vehicle_item_data_deserialization():
    deserializer = VehicleItemDataDeserializer()
    vehicle_item_data = deserializer.load({
        'key': 5,
        'make': 'Foo',
        'model': 'Bar',
        'year': 1987
    })
    assert isinstance(vehicle_item_data, VehicleItemData)
    assert vehicle_item_data.item_key() == 5
    assert vehicle_item_data.make == 'Foo'
    assert vehicle_item_data.model == 'Bar'
    assert vehicle_item_data.year == 1987
