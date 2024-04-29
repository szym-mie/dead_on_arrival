from abc import abstractmethod

from src.entity.item import Item


class Weapon(Item):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def use(self):
        pass

    @abstractmethod
    def can_be_used(self):
        pass

    @abstractmethod
    def remaining_ammo(self):
        pass
