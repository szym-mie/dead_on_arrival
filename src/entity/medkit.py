from src.entity.item import Item
class MedKit(Item):

    def __init__(self,name,  heal_percentage:float):
        super().__init__(name)
        self.heal_percentage = heal_percentage

