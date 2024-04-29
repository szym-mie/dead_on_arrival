from src.entity.weapon import Weapon


class MeleeWeapon(Weapon):
    def remaining_ammo(self):
        return 0

    def can_be_used(self):
        return True

    def use(self):
        pass

    def __init__(self, name):
        super().__init__(name)
