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
        if loi in self:
            self[loi].create_item(item, score)

    def add(self, **kwargs):
        loi = kwargs['loi']
        points = kwargs['points']
        item = kwargs['item'] if 'item' in kwargs else None
        if loi in self:
            self[loi].add(points, item)

    def subtract(self, **kwargs):
        loi = kwargs['loi']
        points = kwargs['points']
        item = kwargs['item'] if 'item' in kwargs else None
        if loi in self:
            self[loi].subtract(points, item)
    
    def disable(self, **kwargs):
        loi = kwargs['loi']
        del self[loi]
    
    def as_profile(self, mapping):
        profile = {}
        for loi, score in self.items():
            profile[loi] = score.mapped_with(mapping)
        return profile
