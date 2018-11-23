class OriginAdvisorError(Exception):
    pass

class InvalidRiskScoreOperation(OriginAdvisorError):
    "Tried to create, add to or remove from items inside a single item score"

class ItemDataKeyNotUnique(OriginAdvisorError):
    "Duplicated item data key"

class MissingKeyDeserializationError(OriginAdvisorError):
    def __init__(self, key):
        self.key = key
    
    def __str__(self):
        return 'missing key "{}" in serialized object'.format(self.key)

class WrongKeyTypeDeserializationError(OriginAdvisorError):
    def __init__(self, key, actual_type, expected_type):
        self.key = key
        self.actual_type = actual_type
        self.expected_type = expected_type
    
    def __str__(self):
        return 'key "{}" in serialized object has wrong type "{}" (expected "{}") '.format(self.key, self.actual_type, self.expected_type)
