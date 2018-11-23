import datetime
from enum import Enum, unique, auto
from .errors import ItemDataKeyNotUnique

@unique
class Gender(Enum):
    male = 'male'
    female = 'female'

    @staticmethod
    def from_str(s):
        if s == 'male':
            return Gender.male
        elif s == 'female':
            return Gender.female
        else:
            raise ValueError

@unique
class MaritalStatus(Enum):
    single = 'single'
    married = 'married'

    @staticmethod
    def from_str(s):
        if s == 'single':
            return MaritalStatus.single
        elif s == 'married':
            return MaritalStatus.married
        else:
            raise ValueError

@unique
class HouseStatus(Enum):
    owned = 'owned'
    mortgaged = 'mortgaged'

    @staticmethod
    def from_str(s):
        if s == 'owned':
            return HouseStatus.owned
        elif s == 'mortgaged':
            return HouseStatus.mortgaged
        else:
            raise ValueError

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
        return [v for v in self._item_data_for_key.values()]

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

class VehicleItemData(ItemData):
    def __init__(self, key, **kwargs):
        super().__init__(key)
        self.make = kwargs['make']
        self.model = kwargs['model']
        self.year = kwargs['year']
    
    def years_since_production(self, curr_date): # FIXME date calculation is not correct.
        """Returns a decimal (float) number of years, 
        counted in days since `curr_date`."""
        production_date = datetime.date(self.year, 1, 1)
        delta = curr_date - production_date
        years = delta.days / 365.0
        return years

class UserData:
    def __init__(self, **kwargs):
        self.age = kwargs['age']
        self.gender = kwargs['gender']
        self.marital_status = kwargs['marital_status']
        self.dependents = kwargs['dependents']
        self.income = kwargs['income']
        self.risk_questions = kwargs['risk_questions']
        # Why inject ItemDataCollection?
        self.house_collec = kwargs['houses']
        self.vehicle_collec = kwargs['vehicles']

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
    
    def get_house_at(self, index):
        house_items = [h for h in self.house_collec.items()]
        return house_items[index]
    
    def get_vehicle_at(self, index):
        vehicle_items = [v for v in self.vehicle_collec.items()]
        return vehicle_items[index]
    
    def has_mortgaged_houses(self):
        return len(self.get_mortgaged_houses()) > 0

    def houses(self):
        return self.house_collec.items()
    
    def houses_count(self):
        return len(self.house_collec)

    def vehicles(self):
        return self.vehicle_collec.items()
    
    def vehicles_count(self):
        return len(self.vehicle_collec)

    def has_dependents(self):
        return self.dependents > 0