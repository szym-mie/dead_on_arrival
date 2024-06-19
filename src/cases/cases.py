from typing import Any
from src.entity.item import Item
from dataclasses import dataclass
from random import randint, shuffle
from src.entity.medkit import MedKit
from src.entity.create_weapon import create_weapon
from src.resource.default_resource_packs import base_pack
@dataclass
class CaseItem:
    # TODO make image for case items
    type: Item
    image: Any = None
    weight: int = 1

    def __repr__(self):
        return f'CaseItem: {self.type.name}'

@dataclass
class Case:

    case_name:str
    items: list[CaseItem]
    items_num = 100
    key_cost = 100


    def create_draw_item_list(self):
        return [item.type for item in self.items for _ in range(item.weight)]

    def open(self, player_budget: int):
        if self.key_cost > player_budget:
            print(f'Not enough score to open the case')
        return self.draw_item()

    def draw_item(self):
        items_to_draw  = self.create_draw_item_list()

        shuffle(items_to_draw)

        drawn_item_idx =  randint(1, self.items_num-1)
        return items_to_draw[drawn_item_idx]


tracer_image = base_pack.get('tex.proj.tracer-oran0')

items = [
    CaseItem(type=create_weapon("ln-87", tracer_image), weight=3),
    CaseItem(type=create_weapon("pb", tracer_image), weight=20),
    CaseItem(type=create_weapon('medkit', tracer_image), weight=30),
    CaseItem(type=create_weapon("Axe", tracer_image), weight=20),
    CaseItem(type=create_weapon('6n4.json', tracer_image), weight=7),
    CaseItem(type=create_weapon('k2000', tracer_image), weight=8),
    CaseItem(type=create_weapon('vls', tracer_image), weight=2),
    CaseItem(type=create_weapon('mk5', tracer_image), weight=9),
    CaseItem(type=create_weapon('oc-15', tracer_image), weight=1),

]


case_1 = Case("default_case",items)


for it in case_1.items:
    print(it)
cnt = 0
item = MedKit(name='medkit', heal_percentage=0.2)
for i in range(100):
    drawn_item = case_1.open(101)
    if drawn_item.name == item.name:
        cnt += 1

print(f'{item} percentage of occurrence: {cnt/case_1.items_num}')
















