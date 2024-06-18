from src.animation.animation import Animation
from src.animation.animation_frame import AnimationFrame
from src.graphics.rect_prototype import RectPrototype
from src.graphics.texture_2d_array import Texture2DArray


class AnimationPrototype:
    def __init__(self, config):
        mesh = config.get('mesh') or {}
        self.mesh_position = mesh.get('position')
        self.mesh_rotation = mesh.get('rotation')
        self.mesh_scale = mesh.get('scale')

        frame_configs = config.get('frames') or []
        self.frames = [AnimationFrame(frame_config) for frame_config in frame_configs]
        self.rect_prototype = None
        self.texture_array = None

    def get_texture_res_ids(self):
        return [frame.texture for frame in self.frames]

    def update_texture(self, textures):
        self.texture_array = Texture2DArray(textures)
        self.rect_prototype = RectPrototype(self.texture_array)

    def get_rect(self):
        return self.rect_prototype.create_mesh(
            self.mesh_position,
            self.mesh_rotation,
            self.mesh_scale
        )

    def create_animation(self):
        return Animation(self)
