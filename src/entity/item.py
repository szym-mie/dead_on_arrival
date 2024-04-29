from src.entity.entity import Entity


class Item(Entity):
    def __init__(self):
        super().__init__()
        self.get_velocity_loss = self.get_item_drag
        self.is_picked_up = False

    def on_grab(self, entity):
        self.is_picked_up = True

    def on_drop(self, entity):
        self.is_picked_up = False
