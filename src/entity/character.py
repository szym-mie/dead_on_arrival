from math import cos, sin, atan2, copysign, pi, sqrt
from src.algorithms.pathfinding import PathFinder
from pyglet.math import Vec3

from src.entity.entity import Entity


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

        self.level_map = None
        self.path = []
        self.path_index = 0

        self.is_shooting = False




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
        if self.is_shooting:
            return
        path_finder = PathFinder(self.level_map)
        if not self.path or self.path_index >= len(self.path):
            self.path = path_finder.get_shortest_path((int(self.position.x), int(self.position.y)), player_position)
            self.path_index = 0

        if self.path:
            target_pos = Vec3(self.path[self.path_index][0], self.path[self.path_index][1], 0)
            direction = target_pos - self.position
            distance_to_target = direction.mag
            step_distance = self.move_speed * delta_time
            self.rotation = atan2(direction.y, direction.x) - pi / 2

            if self.path_index > 15:

                self.path_index = 0


                if path_finder.can_hear((int(self.position.x), int(self.position.y)), player_position,30):

                        self.path = path_finder.get_shortest_path((int(self.position.x), int(self.position.y)), player_position)

                else:
                    self.path = path_finder.get_patrol_path((int(self.position.x), int(self.position.y)))



            if distance_to_target > step_distance:
                direction = direction.normalize()
                self.position += direction * step_distance
            else:
                self.position = target_pos
                self.path_index += 1

            self.update_motion(delta_time)



    def line_of_sight(self, start: Vec3, end: Vec3) -> bool:
        x1, y1 = int(start.x), int(start.y)
        x2, y2 = int(end.x), int(end.y)
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        sx = copysign(1, x2 - x1)
        sy = copysign(1, y2 - y1)
        err = dx - dy

        while True:
            if self.level_map.get_tile_at(x1, y1).is_solid:
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

    def can_see_player(self, player_position: Vec3) -> bool:

        distance_to_player = sqrt(
            (player_position.x - self.position.x) ** 2 + (player_position.y - self.position.y) ** 2)
        if distance_to_player < 1.0:
            return False

        return self.line_of_sight(self.position, player_position)

    def start_shooting(self):
        if self.weapon is not None:
            self.weapon.start_use()
            self.is_shooting = True


    def stop_shooting(self):
        if self.weapon is not None:
            self.weapon.stop_use()
            self.is_shooting = False



    def update_(self,player_position,delta_time):
            super().update(delta_time)
            self.move(player_position,delta_time)



            if self.can_see_player(Vec3(player_position[0], player_position[1], 0)):
                self.start_shooting()
            else:
                self.stop_shooting()

            self.update_weapon_offset()
