from abc import abstractmethod

from pyglet.media import Player

from src.entity.item import Item
from src.entity.projectile import Projectile
from src.entity.world import world
from src.resource.default_resource_packs import base_pack


class Weapon(Item):
    # TODO use dict.get to retrieve values without KeyErrors

    def __init__(self, weapon_config, tracer_rect_proto):
        super().__init__(weapon_config['name'])
        self.weapon_type = weapon_config['type']
        self.weapon_class = weapon_config['class']

        self.tracer_rect_proto = tracer_rect_proto

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

        self.click_sound = base_pack.get('snd.wpn.click')
        self.shot_sound = base_pack.get(self.sounds['shot'])
        self.shot_last_sound = base_pack.get(self.sounds['shot_last'])

        self.sound_player = Player()

    def start_use(self):
        if self.can_be_used() and self.rounds_to_fire == 0:
            self.is_used = True
            self.rounds_to_fire = self.fire_count
            self.fire_time = 0.0
        elif self.rounds_to_fire == 0:
            self.sound_player.next_source()
            self.sound_player.queue(self.click_sound)
            self.sound_player.seek(0)
            self.sound_player.play()

    def stop_use(self):
        self.is_used = False

    def fire(self):
        if self.rounds_to_fire > 0 and self.can_be_used():
            self.sound_player.next_source()
            if (self.rounds_to_fire > 1 or self.fire_count == 1) and self.ammo_count > 1:
                self.sound_player.queue(self.shot_sound)
            else:
                self.sound_player.queue(self.shot_last_sound)
            self.rounds_to_fire -= 1
            self.ammo_count -= 1
            print(self.ammo_count)
            self.sound_player.seek(0)
            self.sound_player.play()

            proj = Projectile(base_pack.get(self.ammo_type), self.tracer_rect_proto)

            world.spawn(proj, self.position.x, self.position.y, 0.0)
            proj.shoot(self.rotation)

            if self.fire_mode == 'auto' and self.is_used:
                self.rounds_to_fire = self.fire_count

            return True
        return False

    @abstractmethod
    def can_be_used(self):
        pass

    @abstractmethod
    def remaining_ammo(self):
        pass

    def update(self, delta_time):
        self.time += delta_time
        self.update_motion(delta_time)
        if self.rounds_to_fire > 0:
            self.fire_time += delta_time
            while self.fire_time > 0:
                self.fire()
                self.fire_time -= self.fire_delay

        # new_fire_time = self.fire_time + delta_time
        # while new_fire_time > self.fire_delay:
        #     self.fire()
        #     new_fire_time -= self.fire_delay
        # self.fire_time = new_fire_time
        # print(self, self.fire_time)
