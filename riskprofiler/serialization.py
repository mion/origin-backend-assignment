# In practice I would take the time to read through marshmallow's
# documentation and use, writing a serializer for this from scratch
# only made sense here because I'm in a hurry.
#
# from marshmallow import Schema, fields
#
from .user_data import UserData, ItemDataCollection, ItemData, VehicleItemData, HouseItemData
from .errors import MissingKeyDeserializationError, WrongKeyTypeDeserializationError

def fetch(obj, key, _type):
    if key in obj:
        if type(obj[key]) == _type:
            return obj[key]
        else:
            raise WrongKeyTypeDeserializationError(key, type(obj[key]), _type)
    else:
        raise MissingKeyDeserializationError(key)

class HouseItemDataDeserializer:
    def load(self, obj):
        key = fetch(obj, 'key', int)
        zip_code = fetch(obj, 'zip_code', int)
        status = fetch(obj, 'status', str)
        return None

class UserDataDeserializer:
    def load(self, obj):
        age = fetch(obj, 'age', int)
        gender = fetch(obj, 'gender', str)
        marital_status = fetch(obj, 'marital_status', str)
        dependents = fetch(obj, 'dependents', int)
        income = fetch(obj, 'income', int)
        houses = fetch(obj, 'houses', list)
        return None
