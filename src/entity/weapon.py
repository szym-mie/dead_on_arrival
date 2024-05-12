from abc import abstractmethod
from src.entity.item import Item
from src.entity.melee_weapon import MeleeWeapon
from src.entity.ranged_weapon import RangedWeapon
from src.resource.default_resource_packs import base_pack


class Weapon(Item):
    configs_getter = base_pack.unit_getter('stat.wpn')

    def __init__(self, weapon_config):
        super().__init__(weapon_config['name'])
        self.weapon_type = weapon_config['type']
        self.weapon_class = weapon_config['class']

        self.ammo_count_max = weapon_config['ammo_count']
        self.ammo_count = self.ammo_count_max

        self.ammo_type = weapon_config['ammo_type']

        self.fire_mode = weapon_config['fire_mode']
        self.fire_count = weapon_config['fire_count']
        self.fire_rate = weapon_config['fire_rate']

        self.fx = weapon_config['fx']
        self.frames = weapon_config['frames']
        self.sounds = weapon_config['sounds']

    @abstractmethod
    def use(self):
        pass

    @abstractmethod
    def can_be_used(self):
        pass

    @abstractmethod
    def remaining_ammo(self):
        pass

    @staticmethod
    def create_weapon(weapon_id):
        config = Weapon.configs_getter(weapon_id)
        if config['type'] == 'melee':
            return MeleeWeapon(config)
        elif config['type'] == 'ranged':
            return RangedWeapon(config)