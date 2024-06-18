import random
from math import cos, sin, atan2, copysign, pi, sqrt
from src.algorithms.pathfinding import PathFinder
from pyglet.math import Vec3

from src.entity.entity import Entity
from src.entity.world import world


class Character(Entity):
    # TODO use dict.get to retrieve values without KeyErrors

    def __init__(self, config):
        super().__init__()

        self.weapon = None
        self.weapon_position = Vec3()

        self.drag = 20

        self.health_max = config['hp']
        self.armor_max = config['ap']

        self.health = self.health_max
        self.armor = self.armor_max

        self.move_speed = config['move_speed']

        self.frames = config['anim']

        self.is_dead = False

        self.state = 'idle'
        self.state_time = 0.0

        self.is_dead = False
        self.is_shooting = False

        self.real_player = None

        self.level_map = world.level
        self.path = []
        self.path_index = 0
        self.wpts = []

        self.path_finder = PathFinder(world.level)

    def deal_damage(self, damage):
        if self.armor > 0:
            self.armor -= damage.get('1', 0)
            self.armor = max(self.armor, 0)
        else:
            self.health -= damage.get('0', 0)
            if self.health <= 0:
                self.is_dead = True

    def update_weapon_offset(self):
        if self.weapon is not None:
            weapon_offset = Vec3(0.25, 0.4, 0.0)
            # weapon_offset = self.weapon.offset

            weapon_offset_rotated = Vec3(
                cos(-self.rotation) * weapon_offset.x + sin(-self.rotation) * weapon_offset.y,
                -sin(-self.rotation) * weapon_offset.x + cos(-self.rotation) * weapon_offset.y,
                0.0
            )
            self.weapon_position = self.position + weapon_offset_rotated

            self.weapon.position = self.weapon_position
            self.weapon.rotation = self.rotation

    def move(self, player_position, delta_time):

        if not self.path_finder.wpts:
            self.path_finder.wpts = self.wpts

        if self.is_shooting:
            return

        if not self.path or self.path_index >= len(self.path):

            self.path = self.path_finder.get_shortest_path(self.position_to_int_vec2D(self.position),
                                                           self.position_to_int_vec2D(player_position))
            self.path_index = 0
            if not self.path:
                self.path = [self.position]

        if self.path:

            target_pos = Vec3(self.path[self.path_index][0], self.path[self.path_index][1], 0)
            direction = target_pos - self.position
            distance_to_target = direction.mag
            step_distance = self.move_speed * delta_time
            self.rotation = atan2(direction.y, direction.x) - pi / 2

            if self.path_index > 30:

                if self.path_finder.can_hear(self.position_to_int_vec2D(self.position),
                                             self.position_to_int_vec2D(player_position), 30):
                    print("Can hear")
                    if random.randint(1, 10) < 3:
                        self.path = self.path_finder.flank(self.position_to_int_vec2D(self.position),
                                                           self.position_to_int_vec2D(player_position))
                    else:

                        self.path = self.path_finder.get_shortest_path(self.position_to_int_vec2D(self.position),
                                                                       self.position_to_int_vec2D(player_position))

                    self.path_index = 0

                else:
                    print("Patrol")
                    self.path = self.path_finder.get_patrol_path(self.position_to_int_vec2D(self.position))
                    self.path_index = 0

            if distance_to_target > step_distance:
                direction = direction.normalize()
                self.position += direction * step_distance
            else:
                self.position = target_pos
                self.path_index += 1

            self.update_motion(delta_time)

    def line_of_sight(self, start: Vec3, end: Vec3) -> bool:
        x1, y1 = self.position_to_int_vec2D(start)
        x2, y2 = self.position_to_int_vec2D(end)
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        sx = copysign(1, x2 - x1)
        sy = copysign(1, y2 - y1)
        err = dx - dy

        while True:
            tile = self.level_map.get_tile_at(x1, y1)
            if tile is None or tile.is_solid:
                return False
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
        return True

    @staticmethod
    def angle_normalize(angle):
        mod_angle = angle % (pi * 2)
        return mod_angle if mod_angle < pi else pi * 2 - mod_angle

    @staticmethod
    def position_to_int_vec2D(position):
        return int(position.x), int(position.y)

    def can_see_player(self, player_position: Vec3) -> bool:
        dx = player_position.x - self.position.x
        dy = player_position.y - self.position.y
        direction = Character.angle_normalize(-atan2(dx, dy) - self.rotation)
        if -1.5 < direction < 1.5:
            distance_to_player = sqrt(dx ** 2 + dy ** 2)
            if distance_to_player < 1.0:
                return False

            return self.line_of_sight(self.position, player_position)
        return False

    def start_shooting(self):
        self.set_state('shoot')
        if self.weapon is not None:
            self.weapon.start_use()
            self.is_shooting = True

    def stop_shooting(self):
        self.set_state('idle')
        if self.weapon is not None:
            self.weapon.stop_use()
            self.is_shooting = False

    def set_state(self, state):
        if self.state == state:
            return False
        self.state = state
        self.state_time = 0.0
        return True

    def update_(self, player_position, delta_time):
        super().update(delta_time)
        self.state_time += delta_time

        self.move(player_position, delta_time)

        if self.can_see_player(player_position):
            dx = self.position.x - player_position.x
            dy = self.position.y - player_position.y
            self.rotation = atan2(dy, dx) + pi / 2
            if self.state_time > 1.5:
                self.start_shooting()
        if self.state == 'shoot' and self.state_time > 0.5:
            self.stop_shooting()

        self.update_weapon_offset()
