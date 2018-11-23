# In practice I would take the time to read through the docs of a 
# serialization lib (e.g. marshmallow) and use it. Writing a "quick and 
# dirty" serializer for this from scratch only made sense here
# because I'm under a time constraint.
from riskprofiler.user_data import UserData, ItemData, ItemDataCollection, VehicleItemData, HouseItemData, Gender, MaritalStatus, HouseStatus
from .errors import MissingKeyDeserializationError, WrongKeyTypeDeserializationError

def fetch(obj, key, _type):
    if key in obj:
        if type(obj[key]) == _type:
            return obj[key]
        else:
            raise WrongKeyTypeDeserializationError(key, type(obj[key]), _type)
    else:
        raise MissingKeyDeserializationError(key)

class VehicleItemDataDeserializer:
    def load(self, obj):
        key = fetch(obj, 'key', int)
        make = fetch(obj, 'make', str)
        model = fetch(obj, 'model', str)
        year = fetch(obj, 'year', int)
        return VehicleItemData(key, make=make, model=model, year=year)

class HouseItemDataDeserializer:
    def load(self, obj):
        key = fetch(obj, 'key', int)
        zip_code = fetch(obj, 'zip_code', int)
        status = HouseStatus.from_str(fetch(obj, 'status', str))
        return HouseItemData(key, zip_code=zip_code, status=status)

class UserDataDeserializer:
    def load(self, obj):
        age = fetch(obj, 'age', int)
        gender = Gender.from_str(fetch(obj, 'gender', str))
        marital_status = MaritalStatus.from_str(fetch(obj, 'marital_status', str))
        dependents = fetch(obj, 'dependents', int)
        income = fetch(obj, 'income', int)
        houses_obj = fetch(obj, 'houses', list)
        houses = ItemDataCollection(*[HouseItemDataDeserializer().load(h) for h in houses_obj])
        vehicles_obj = fetch(obj, 'vehicles', list)
        vehicles = ItemDataCollection(*[VehicleItemDataDeserializer().load(v) for v in vehicles_obj])
        risk_questions = fetch(obj, 'risk_questions', list)
        return UserData(
            age=age,
            gender=gender,
            marital_status=marital_status,
            dependents=dependents,
            income=income,
            houses=houses,
            vehicles=vehicles,
            risk_questions=risk_questions
        )

class RiskProfileSerializer:
    def to_dict(self, risk_profile):
        obj = {}
        for loi, val in risk_profile.items():
            if isinstance(val, dict):
                obj[loi.value] = [{'key': item_key, 'value': aversion.value} for item_key, aversion in val.items()]
            else:
                obj[loi.value] = val.value
        return obj
