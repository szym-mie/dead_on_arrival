from src.entity.weapon import Weapon


class RangedWeapon(Weapon):
    def __init__(self, config, tr):
        super().__init__(config, tr)

    def can_be_used(self):
        return self.ammo_count > 0

    def remaining_ammo(self):
        return self.ammo_count


