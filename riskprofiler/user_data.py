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
    def __init__(self, *args):
        self._item_data_for_key = {}
        for item_data in args:
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
        self.zip_code = kwargs['zip_code']
        self.status = kwargs['status']

    @staticmethod
    def parse(json):
        key = json['key']
        zip_code = json['zip']
        status = HouseStatus.parse(json['status'])
        return HouseItemData(key, zip_code=zip_code, status=status)

class VehicleItemData(ItemData):
    def __init__(self, key, **kwargs):
        super().__init__(key)
        self.make = kwargs['make']
        self.model = kwargs['model']
        self.year = kwargs['year']

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
        self.age = kwargs['age']
        self.gender = kwargs['gender']
        self.marital_status = kwargs['marital_status']
        self.dependents = kwargs['dependents']
        self.income = kwargs['income']
        self.house_collec = kwargs['houses']
        self.vehicle_collec = kwargs['vehicles']
        self.risk_questions = kwargs['risk_questions']

    def base_score(self):
        return sum(self.risk_questions)
    
    def is_married(self):
        return self.marital_status == MaritalStatus.married

    def has_income(self):
        return self.income > 0
    
    def is_income_above(self, value):
        return self.income > value

    def is_under_age(self, target_age):
        return self.age < target_age

    def is_over_age(self, target_age):
        return self.age > target_age

    def has_vehicles(self):
        return len(self.vehicle_collec) > 0

    def has_houses(self):
        return len(self.house_collec) > 0

    def get_mortgaged_houses(self):
        return [h for h in self.house_collec.items() if h.status == HouseStatus.mortgaged]
    
    def has_mortgaged_houses(self):
        return len(self.get_mortgaged_houses()) > 0

    def houses(self):
        return self.house_collec.items()

    def vehicles(self):
        return self.vehicle_collec.items()

    def has_dependents(self):
        return self.dependents > 0