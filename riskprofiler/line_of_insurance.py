from enum import Enum, unique

@unique
class Loi(Enum):
    """Line of insurance"""
    life = 'life'
    disability = 'disability'
    home = 'home'
    auto = 'auto'

    @staticmethod
    def all_lines():
        return (Loi.life, Loi.disability, Loi.home, Loi.auto)
