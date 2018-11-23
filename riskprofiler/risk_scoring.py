from enum import Enum, unique
from .errors import InvalidRiskScoreOperation

class _SingleItemRiskScore:
    def __init__(self, value):
        self.value = value

    def create_item(self, *args):
        raise InvalidRiskScoreOperation

    def add(self, points, key):
        if key is not None:
            raise InvalidRiskScoreOperation
        self.value += points

    def subtract(self, points, key):
        if key is not None:
            raise InvalidRiskScoreOperation
        self.value -= points
    
    def mapped_with(self, mapping):
        return mapping.map_score_value(self.value)

class _MultipleItemRiskScore(dict):
    def create_item(self, key, value):
        self[key] = value

    def subtract_from(self, key, points):
        self[key] -= points

    def add(self, points, key):
        if key is None:
            for key, _ in self.items():
                self[key] += points
        else:
            self[key] += points

    def subtract(self, points, key):
        if key is None:
            for key, _ in self.items():
                self[key] -= points
        else:
            self[key] -= points

    def mapped_with(self, mapping):
        mapped = {}
        for key, value in self.items():
            mapped[key] = mapping.map_score_value(value)
        return mapped

class RiskScoring(dict):
    def create(self, **kwargs):
        loi = kwargs['loi']
        multiple_items = kwargs['multiple_items'] if 'multiple_items' in kwargs else False
        if multiple_items:
            self[loi] = _MultipleItemRiskScore()
        else:
            score = kwargs['score']
            self[loi] = _SingleItemRiskScore(score)

    def create_item(self, **kwargs):
        loi = kwargs['loi']
        item = kwargs['item']
        score = kwargs['score']
        self[loi].create_item(item, score)

    def add(self, **kwargs):
        loi = kwargs['loi']
        points = kwargs['points']
        item = kwargs['item'] if 'item' in kwargs else None
        self[loi].add(points, item)

    def subtract(self, **kwargs):
        loi = kwargs['loi']
        points = kwargs['points']
        item = kwargs['item'] if 'item' in kwargs else None
        self[loi].subtract(points, item)
    
    def disable(self, **kwargs):
        loi = kwargs['loi']
        del self[loi]
    
    def as_profile(self, mapping):
        profile = {}
        for loi, score in self.items():
            profile[loi] = score.mapped_with(mapping)
        return profile

@unique
class RiskAversion(Enum):
    conservative = 'conservative'
    average = 'average'
    adventurous = 'adventurous'

class RiskScoreValueMapping:
    def map_score_value(self, score_value):
        if score_value <= 0:
            return RiskAversion.adventurous
        elif score_value == 1 or score_value == 2:
            return RiskAversion.average
        else:
            return RiskAversion.conservative

class RiskProfileCalculator:
    def __init__(self, **kwargs):
        self.user_data = kwargs['user_data']
        self.policies = kwargs['risk_policies']
        self.scoring = kwargs['risk_scoring']
        self.mapping = kwargs['risk_score_value_mapping']
    
    def calculate(self):
        for policy in self.policies:
            policy.apply(self.scoring)
        return self.scoring.as_profile(self.mapping)