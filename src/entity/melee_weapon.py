from src.entity.weapon import Weapon
from src.entity.world import world


class MeleeWeapon(Weapon):
    def __init__(self, config):
        super().__init__(config)

    def remaining_ammo(self):
        return 0

    def can_be_used(self):
        return True

    def use(self):
        world
