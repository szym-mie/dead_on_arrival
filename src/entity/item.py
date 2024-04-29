from src.entity.entity import Entity


class Item(Entity):
    def __init__(self,name):
        super().__init__()
        self.get_velocity_loss = self.get_item_drag
        self.is_picked_up = False
        self.name = name

    def on_grab(self, entity):
        self.is_picked_up = True

    def on_drop(self, entity):
        self.is_picked_up = False


    def __repr__(self):
        return f'Item: {self.name}'
