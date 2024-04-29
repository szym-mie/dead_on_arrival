from src.entity.entity import Entity


class Projectile(Entity):
    def __init__(self):
        super().__init__()
        self.get_velocity_loss = self.get_projectile_drag


