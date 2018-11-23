from enum import Enum, unique
from .risk_scoring import RiskScoring
from .risk_policies import InitialRiskPolicy, NoIncomePolicy, NoVehiclePolicy, NoHousePolicy, AgePolicy, LargeIncomePolicy, MortgagedHousePolicy, DependentsPolicy, MaritalStatusPolicy, RecentVehiclePolicy, SingleHousePolicy, SingleVehiclePolicy

CURRENT_RISK_POLICIES = [
    InitialRiskPolicy(),
    NoIncomePolicy(),
    NoVehiclePolicy(),
    NoHousePolicy(),
    AgePolicy(),
    LargeIncomePolicy(),
    MortgagedHousePolicy(),
    DependentsPolicy(),
    MaritalStatusPolicy(),
    RecentVehiclePolicy(),
    SingleHousePolicy(),
    SingleVehiclePolicy()
]

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
        self.policies = CURRENT_RISK_POLICIES if 'risk_policies' not in kwargs else kwargs['risk_policies']
        self.scoring = RiskScoring() if 'risk_scoring' not in kwargs else kwargs['risk_scoring']
        self.mapping = RiskScoreValueMapping() if 'risk_score_value_mapping' not in kwargs else kwargs['risk_score_value_mapping']
    
    def calculate(self):
        for policy in self.policies:
            policy.apply(self.user_data, self.scoring)
        return self.scoring.as_profile(self.mapping)
