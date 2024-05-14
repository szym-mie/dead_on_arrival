from src.entity.melee_weapon import MeleeWeapon
from src.entity.ranged_weapon import RangedWeapon
from src.resource.default_resource_packs import base_pack
from src.util.console import console

configs_getter = base_pack.unit_getter('stat.wpn')


def create_weapon(weapon_id):
    config = configs_getter(weapon_id)
    weapon_type = config.get('type')
    if weapon_type == 'melee':
        return MeleeWeapon(config)
    elif weapon_type == 'ranged':
        return RangedWeapon(config)
    else:
        console.log_warn('unknown weapon type' + weapon_type)
