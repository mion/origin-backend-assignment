from enum import Enum, unique

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
