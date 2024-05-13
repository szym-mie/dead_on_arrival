from src.entity.entity import Entity


class Character(Entity):
    # TODO use dict.get to retrieve values without KeyErrors

    def __init__(self, config):
        super().__init__()

        self.weapon = None

        self.drag = 20

        self.health_max = config['hp']
        self.armor_max = config['ap']

        self.health = self.health_max
        self.armor = self.armor_max

        self.move_speed = config['move_speed']

        self.frames = config['anim']

        self.is_dead = False
