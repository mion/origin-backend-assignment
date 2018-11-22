class OriginAdvisorError(Exception):
    pass

class InvalidRiskScoreOperation(OriginAdvisorError):
    "Tried to create, add to or remove from items inside a single item score"

class ItemDataKeyNotUnique(OriginAdvisorError):
    "Duplicated item data key"