from enum import Enum, unique

@unique
class RiskAversion(Enum):
    conservative = 'conservative'
    average = 'average'
    adventurous = 'adventurous'

class RiskAversionMapping:
    def aversion_for(self, score_value):
        if score_value <= 0:
            return RiskAversion.adventurous
        elif score_value == 1 or score_value == 2:
            return RiskAversion.average
        else:
            return RiskAversion.conservative

class RiskProfile:
    def __init__(self, **kwargs):
        self.user_data = getattr(kwargs, 'user_data')
        self.policy_set = getattr(kwargs, 'policy_set')
        self.risk_scoring = getattr(kwargs, 'risk_scoring')
        self.risk_aversion_mapping = getattr(kwargs, 'risk_aversion_mapping')
    
    def compute(self):
        final_risk_scoring = self.policy_set.apply_all(self.user_data, self.risk_scoring)
        return final_risk_scoring.to_profile(self.risk_aversion_mapping)
