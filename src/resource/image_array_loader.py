import json
from typing import Any

from src.resource.loader import Loader, register_loader


class ImageArraySource:
    def __init__(self, image_array_res_ids):
        self.image_array_res_ids = image_array_res_ids

    def get_texture_res_ids(self):
        array = [None] * len(self.image_array_res_ids)
        for index, res_id in self.image_array_res_ids.items():
            array[int(index)] = res_id

        return array


@register_loader('image_array')
class ImageArrayLoader(Loader):
    def load(self, resource_manager) -> Any:
        image_array_source = \
            self.map_open('text', lambda p, f: ImageArraySource(json.load(f)))
        textures = \
            [resource_manager.get(tex_id) for tex_id in image_array_source.get_texture_res_ids()]
        return textures
