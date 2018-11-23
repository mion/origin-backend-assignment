from .errors import InvalidRiskScoreOperation

class SingleItemRiskScore:
    def __init__(self, score):
        self.score = score

    def create_item(self, *args):
        raise InvalidRiskScoreOperation

    def add(self, points, item):
        if item is not None:
            raise InvalidRiskScoreOperation
        self.score += points

    def subtract(self, points, item):
        if item is not None:
            raise InvalidRiskScoreOperation
        self.score -= points

    def map_aversion(self, mapping):
        return mapping.aversion_for(self.score)

class MultipleItemRiskScore:
    def __init__(self):
        self.score_for_item = {}

    def create_item(self, item, item_score):
        self.score_for_item[item] = item_score

    def subtract_from(self, item, points):
        self.score_for_item[item] -= points

    def add(self, points, item):
        if item is None:
            for item, _ in self.score_for_item.items():
                self.score_for_item[item] += points
        else:
            self.score_for_item[item] += points

    def subtract(self, points, item):
        if item is None:
            for item, _ in self.score_for_item.items():
                self.score_for_item[item] -= points
        else:
            self.score_for_item[item] -= points

    def map_aversion(self, mapping):
        aversion_for_item = {}
        for item, score_value in self.score_for_item.items():
            aversion_for_item[item] = mapping.aversion_for(score_value)
        return aversion_for_item

class RiskScoring:
    def __init__(self, **kwargs):
        self.score_for_loi = {}
        self.disabled_lois = {}

    def create(self, **kwargs):
        loi = kwargs['loi']
        multiple_items = kwargs['multiple_items'] if 'multiple_items' in kwargs else False
        if multiple_items:
            self.score_for_loi[loi] = MultipleItemRiskScore()
        else:
            score = kwargs['score']
            self.score_for_loi[loi] = SingleItemRiskScore(score)

    def create_item(self, **kwargs):
        loi = kwargs['loi']
        item = kwargs['item']
        score = kwargs['score']
        self.score_for_loi[loi].create_item(item, score)

    def add(self, **kwargs):
        loi = kwargs['loi']
        points = kwargs['points']
        item = kwargs['item'] if 'item' in kwargs else None
        self.score_for_loi[loi].add(points, item)

    def subtract(self, **kwargs):
        loi = kwargs['loi']
        points = kwargs['points']
        item = kwargs['item'] if 'item' in kwargs else None
        self.score_for_loi[loi].subtract(points, item)
    
    def disable(self, **kwargs):
        loi = kwargs['loi']
        self.disabled_lois[loi] = True

    def to_profile(self, mapping):
        profile = {}
        for loi, score in self.score_for_loi.items():
            profile[loi] = score.map_aversion(mapping)
        return profile