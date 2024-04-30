from abc import abstractmethod
from pyglet.math import Vec2
from src.entity.item import Item


class Weapon(Item):
    def __init__(self,name:str, damage:int, usage_cooldown:int, weapon_offset:Vec2):
        super().__init__(name)
        self.name = name
        self.damage = damage
        self.usage_cooldown = usage_cooldown
        self.weapon_offset = weapon_offset

    @abstractmethod
    def use(self):
        pass

    @abstractmethod
    def can_be_used(self):
        pass

    @abstractmethod
    def remaining_ammo(self):
        pass
