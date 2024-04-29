from src.entity.weapon import Weapon
from src.world import World


class RangedWeapon(Weapon):
    def __init__(self, ammo):
        super().__init__()
        self.ammo = ammo

    def use(self):
        World.default()

    def can_be_used(self):
        return self.ammo > 0

    def remaining_ammo(self):
        return self.ammo
