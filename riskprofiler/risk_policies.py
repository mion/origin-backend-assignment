from .line_of_insurance import Loi

class RiskPolicySet:
    def __init__(self, **kwargs):
        self.policies = kwargs['policies']

    def apply_all(self, user_data, risk_scoring):
        for pol in self.policies:
            pol.apply(user_data, risk_scoring)
        return risk_scoring

class BaseRiskPolicy:
    def apply(self, user_data, risk_scoring):
        raise NotImplementedError('subclass must implement "apply" method')

class InitialRiskPolicy(BaseRiskPolicy):
    def apply(self, user_data, scoring):
        base_score_value = user_data.base_score()

        scoring.create(loi=Loi.life, score=base_score_value)
        scoring.create(loi=Loi.disability, score=base_score_value)

        scoring.create(loi=Loi.home, multiple_items=True)
        for house in user_data.houses():
            scoring.create_item(loi=Loi.home, item=house.key(), score=base_score_value)

        scoring.create(loi=Loi.auto, score=base_score_value, multiple_items=True)
        for vehicle in user_data.vehicles():
            scoring.create_item(loi=Loi.auto, item=vehicle.key(), score=base_score_value)

class NoIncomePolicy(BaseRiskPolicy):
    def apply(self, user_data, scoring):
        if not user_data.has_income():
            scoring.disable(loi=Loi.disability)

class NoVehiclePolicy(BaseRiskPolicy):
    def apply(self, user_data, scoring):
        if not user_data.has_vehicles():
            scoring.disable(loi=Loi.auto)

class NoHousePolicy(BaseRiskPolicy):
    def apply(self, user_data, scoring):
        if not user_data.has_houses():
            scoring.disable(loi=Loi.home)

class AgePolicy(BaseRiskPolicy):
    def apply(self, user_data, scoring):
        if user_data.is_under_age(30):
            for loi in Loi.all_lines():
                scoring.subtract(points=2, loi=loi)
        elif user_data.is_under_age(40):
            for loi in Loi.all_lines():
                scoring.subtract(points=1, loi=loi)
        elif user_data.is_over_age(60):
            scoring.disable(loi=Loi.disability)
            scoring.disable(loi=Loi.life)

class LargeIncomePolicy(BaseRiskPolicy):
    LARGE_INCOME_THRESH = 200000

    def __init__(self, large_income_thresh=LARGE_INCOME_THRESH):
        self.large_income_thresh = large_income_thresh

    def apply(self, user_data, scoring):
        if user_data.is_income_above(self.large_income_thresh):
            for loi in Loi.all_lines():
                scoring.subtract(points=1, loi=loi)

class MortgagedHousePolicy(BaseRiskPolicy):
    def apply(self, user_data, scoring):
        if user_data.has_mortgaged_houses():
            scoring.add(points=1, loi=Loi.disability)
            for house in user_data.get_mortgaged_houses():
                scoring.add(points=1, loi=Loi.home, item=house.item_key())

class DependentsPolicy(BaseRiskPolicy):
    def apply(self, user_data, scoring):
        if user_data.has_dependents():
            scoring.add(points=1, loi=Loi.disability)
            scoring.add(points=1, loi=Loi.life)

class MaritalStatusPolicy(BaseRiskPolicy):
    def apply(self, user_data, scoring):
        if user_data.is_married():
            scoring.add(points=1, loi=Loi.life)
            scoring.subtract(points=1, loi=Loi.disability)

class RecentVehiclePolicy(BaseRiskPolicy):
    NUM_RECENT_YEARS = 5 # FIXME Use time delta, this is incorrect.
    def apply(self, user_data, scoring):
        for vehicle in user_data.get_vehicles():
            if vehicle.years_since_production() <= self.NUM_RECENT_YEARS:
                scoring.add(points=1, loi=Loi.auto, item=vehicle.item_key())

class SingleHousePolicy(BaseRiskPolicy):
    def apply(self, user_data, scoring):
        if user_data.houses_count() == 1:
            house = user_data.get_house_at(0)
            scoring.add(points=1, loi=Loi.home, item=house.item_key())

class SingleVehiclePolicy(BaseRiskPolicy):
    def apply(self, user_data, scoring):
        if user_data.vehicles_count() == 1:
            vehicle = user_data.get_vehicle_at(0)
            scoring.add(points=1, loi=Loi.auto, item=vehicle.item_key())