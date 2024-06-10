import json

from src.animation.animation_prototype import AnimationPrototype
from src.resource.loader import Loader, register_loader


@register_loader('animation')
class AnimationLoader(Loader):
    def load(self, resource_manager):
        animation_prototype = \
            self.map_open('text', lambda p, f: AnimationPrototype(json.load(f)))
        textures = \
            [resource_manager.get(tex_id) for tex_id in animation_prototype.get_texture_res_ids()]
        animation_prototype.update_texture(textures)
        return

