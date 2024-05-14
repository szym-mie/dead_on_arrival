from abc import abstractmethod

from pyglet.media import PlayerGroup, Player

from src.entity.item import Item
from src.resource.default_resource_packs import base_pack


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
        self.rounds_to_fire = 0

        self.fx = weapon_config['fx']
        self.anim = weapon_config['anim']
        self.sounds = weapon_config['sounds']

        self.shot_sound = base_pack.get(self.sounds['shot'])
        self.shot_last_sound = base_pack.get(self.sounds['shot_last'])

        self.player = Player()

    def start_use(self):
        self.is_used = True
        self.rounds_to_fire = self.fire_count
        self.fire_time = 0.0

    def stop_use(self):
        self.is_used = False

    def fire(self):
        if self.rounds_to_fire > 0 and self.can_be_used():
            self.player.next_source()
            if (self.rounds_to_fire > 1 or self.fire_count == 1) and self.ammo_count > 1:
                self.player.queue(self.shot_sound)
            else:
                self.player.queue(self.shot_last_sound)
            self.rounds_to_fire -= 1
            self.ammo_count -= 1
            print(self.ammo_count)
            self.player.seek(0)
            self.player.play()

    @abstractmethod
    def can_be_used(self):
        pass

    @abstractmethod
    def remaining_ammo(self):
        pass

    def update(self, delta_time):
        self.time += delta_time
        self.update_motion(delta_time)
        new_fire_time = self.fire_time + delta_time
        while new_fire_time > self.fire_delay:
            self.fire()
            new_fire_time -= self.fire_delay
        self.fire_time = new_fire_time
