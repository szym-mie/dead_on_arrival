from abc import abstractmethod

from src.entity.item import Item


class Weapon(Item):
    # TODO use dict.get to retrieve values without KeyErrors

    def __init__(self, weapon_config):
        super().__init__(weapon_config['name'])
        self.weapon_type = weapon_config['type']
        self.weapon_class = weapon_config['class']

        self.is_used = False

        self.ammo_count_max = weapon_config['ammo_count']
        self.ammo_count = self.ammo_count_max

        self.ammo_type = weapon_config['ammo_type']

        self.fire_mode = weapon_config['fire_mode']
        self.fire_count = weapon_config['fire_count']
        self.fire_rate = weapon_config['fire_rate']

        self.fire_delay = 60 / self.fire_rate
        self.rounds_to_fire = self.fire_count

        self.fx = weapon_config['fx']
        self.frames = weapon_config['anim']
        self.sounds = weapon_config['sounds']

    def start_use(self):
        self.is_used = True

    def stop_use(self):
        self.is_used = False

    @abstractmethod
    def can_be_used(self):
        pass

    @abstractmethod
    def remaining_ammo(self):
        pass
