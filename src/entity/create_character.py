from src.entity.character import Character
from src.entity.player import Player
from src.resource.default_resource_packs import base_pack

configs_getter = base_pack.unit_getter('stat.char')


def create_character(character_id):
    config = configs_getter(character_id)
    if config.get('is_player'):
        return Player(config)
    else:
        return Character(config)
