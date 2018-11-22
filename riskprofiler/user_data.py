from enum import Enum, unique
from .errors import ItemDataKeyNotUnique

@unique
class Gender(Enum):
    male = 'male'
    female = 'female'

@unique
class MaritalStatus(Enum):
    single = 'single'
    married = 'married'

@unique
class HouseStatus(Enum):
    owned = 'owned'
    mortgaged = 'mortgaged'

class ItemDataCollection:
    def __init__(self, item_datas=[]):
        self._item_data_for_key = {}
        for item_data in item_datas:
            self.add(item_data)

    def __len__(self):
        return len(self._item_data_for_key)

    def add(self, item_data):
        if item_data.item_key() in self._item_data_for_key:
            raise ItemDataKeyNotUnique
        self._item_data_for_key[item_data.item_key()] = item_data

    def items(self):
        return self._item_data_for_key.values()

class ItemData:
    def __init__(self, key):
        self._key = key

    def item_key(self):
        return self._key

class HouseItemData(ItemData):
    def __init__(self, key, **kwargs):
        super().__init__(key)
        self.zip_code = getattr(kwargs, 'zip_code')
        self.status = getattr(kwargs, 'status')

    @staticmethod
    def parse(json):
        key = json['key']
        zip_code = json['zip']
        status = HouseStatus.parse(json['status'])
        return HouseItemData(key, zip_code=zip_code, status=status)

class VehicleItemData(ItemData):
    def __init__(self, key, **kwargs):
        super().__init__(key)
        self.make = getattr(kwargs, 'make')
        self.model = getattr(kwargs, 'model')
        self.year = getattr(kwargs, 'year')

    @staticmethod
    def parse(json):
        key = json['key']
        make = json['make']
        model = json['model']
        year = json['year']
        return VehicleItemData(key, make=make, model=model, year=year)

class RiskQuestionData:
    def __init__(self, value):
        self._value = value

    def value(self):
        return self._value

class UserData:
    def __init__(self, **kwargs):
        self.age = getattr(kwargs, 'age')
        self.gender = getattr(kwargs, 'gender')
        self.marital_status = getattr(kwargs, 'marital_status')
        self.dependents = getattr(kwargs, 'dependents')
        self.income = getattr(kwargs, 'income')
        self.house_collec = getattr(kwargs, 'houses')
        self.vehicle_collec = getattr(kwargs, 'vehicles')
        self.risk_questions = getattr(kwargs, 'risk_questions')

    def base_score(self):
        return sum([q.value() for q in self.risk_questions])

    def has_income(self):
        return self.income > 0

    def is_under_age(self, target_age):
        return self.age < target_age

    def is_over_age(self, target_age):
        return self.age > target_age

    def has_vehicles(self):
        return len(self.vehicle_collec) > 0

    def has_houses(self):
        return len(self.house_collec) > 0

    def has_mortgaged_houses(self):
        mortgaged_houses = [h for h in self.house_collec.items() if h.status == HouseStatus.mortgaged]
        return len(mortgaged_houses) > 0

    def houses(self):
        return self.house_collec.items()

    def vehicles(self):
        return self.vehicle_collec.items()

    def has_dependents(self):
        return self.dependents > 0