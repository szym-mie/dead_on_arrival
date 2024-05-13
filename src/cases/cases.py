from dataclasses import dataclass
from typing import Any
from random import randint, shuffle
from src.entity.melee_weapon import MeleeWeapon
from src.entity.ranged_weapon import RangedWeapon
from src.entity.medkit import MedKit
from src.entity.item import Item
from pyglet.math import Vec2
@dataclass
class CaseItem:
    # TODO make image for case items
    type: Item
    image: Any = None
    weight: int = 1

    def __repr__(self):
        return f'CaseItem: {self.type.name}'


class Case:
    def __init__(self, case_name: str, items_list:list[CaseItem]):
        self.items: list[CaseItem] = items_list
        self.name: str = case_name
        self.items_num = 100
        self.key_cost = 100

    def create_draw_item_list(self):
        return [i.type for i in self.items for _ in range(i.weight)]

    def open(self, player_budget: int):
        if self.key_cost > player_budget:
            print(f'Not enough score to open the case')
        return self.draw_item()

    def draw_item(self):
        items_to_draw  = self.create_draw_item_list()

        shuffle(items_to_draw)

        drawn_item_idx =  randint(1, self.items_num-1)
        return items_to_draw[drawn_item_idx]

items = [
    CaseItem(type=RangedWeapon(name='ln87',ammo=100, damage=4, usage_cooldown=10, weapon_offset=Vec2(10, 10)), weight=3),
    CaseItem(type=RangedWeapon(name='pb', ammo=20, damage=7, usage_cooldown=20, weapon_offset=Vec2(10, 10)), weight=20),
    CaseItem(type=MedKit(name='medkit', heal_percentage=0.2), weight=30),
    CaseItem(type=MeleeWeapon(name="Axe", damage=12, usage_cooldown=30, weapon_offset=Vec2(10, 10)), weight=20),
    CaseItem(type=MeleeWeapon(name='6n4.json', damage=5, usage_cooldown=20, weapon_offset=Vec2(10, 10)), weight=7),
    CaseItem(type=MeleeWeapon(name='k2000', damage=9, usage_cooldown=15, weapon_offset=Vec2(10, 10)), weight=8),
    CaseItem(type=RangedWeapon(name='vls', ammo=30, damage=20, usage_cooldown=11, weapon_offset=Vec2(10, 10)), weight=2),
    CaseItem(type=RangedWeapon(name='mk-5', ammo=80, damage=16, usage_cooldown=8, weapon_offset=Vec2(10, 10)), weight=9),
    CaseItem(type=RangedWeapon(name='oc-15', ammo=44, damage=24, usage_cooldown=19, weapon_offset=Vec2(10, 10)), weight=1),

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
















