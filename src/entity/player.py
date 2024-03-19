from src.entity.entity import Entity
from src.frame.export import frame_method
from src.frame.frame import Frame


class Player(Entity):
    def __init__(self, initial_frame: Frame):
        super().__init__(initial_frame)

    @frame_method
    def wait_fire_weapon(self, target) -> bool:
        pass
