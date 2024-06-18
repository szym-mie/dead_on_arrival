from abc import abstractmethod

from src.entity.entity import Entity


class Item(Entity):
    def __init__(self, name):
        super().__init__()
        self.get_velocity_loss = self.get_item_drag

        self.is_picked_up = False
        self.position.z = -0.5
        self.is_used = False
        self.fire_time = 0.0
        self.name = name

    def on_grab(self, entity):
        self.is_picked_up = True
        self.position.z = 0.1

    def on_drop(self, entity):
        self.is_picked_up = False
        self.position.z = -0.5

    @abstractmethod
    def start_use(self):
        pass

    @abstractmethod
    def stop_use(self):
        pass

    def __repr__(self):
        return f'Item: {self.name}'
