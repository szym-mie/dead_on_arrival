from src.entity.weapon import Weapon
from src.entity.world import World


class RangedWeapon(Weapon):
    def __init__(self,name, ammo, damage, usage_cooldown, weapon_offset):
        super().__init__(name, damage, usage_cooldown, weapon_offset)
        self.ammo = ammo

    def use(self):
        World.default()

    def can_be_used(self):
        return self.ammo > 0

    def remaining_ammo(self):
        return self.ammo


