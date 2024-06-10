from src.animation.animation import Animation
from src.animation.animation_frame import AnimationFrame
from src.graphics.texture_2d_array import Texture2DArray


class AnimationPrototype:
    def __init__(self, config):
        self.frames = [AnimationFrame(frame_config) for frame_config in config]
        self.texture_array = None

    def get_texture_res_ids(self):
        return [frame.texture for frame in self.frames]

    def update_texture(self, textures):
        self.texture_array = Texture2DArray(textures)

    def create_animation(self):
        return Animation(self)
