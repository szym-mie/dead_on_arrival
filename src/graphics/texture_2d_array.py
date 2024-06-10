from ctypes import c_ubyte

from pyglet.gl import *
from pyglet.image import CheckerImagePattern


class Texture2DArray:
    def __init__(self, images):
        self.texture_handler = GLuint()
        glGenTextures(1, self.texture_handler)
        width, height = Texture2DArray._get_texture_array_size(images)

        self.layer_count = len(images)

        glBindTexture(GL_TEXTURE_2D_ARRAY, self.texture_handler)

        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexStorage3D(GL_TEXTURE_2D_ARRAY, 1, GL_RGBA8, width, height, self.layer_count)

        self.set_texture(images)

    def set_texture(self, images):
        glBindTexture(GL_TEXTURE_2D_ARRAY, self.texture_handler)
        width, height = Texture2DArray._get_texture_array_size(images)

        for layer, image in enumerate(images):
            print(layer, image.get_data())
            glTexSubImage3D(GL_TEXTURE_2D_ARRAY, 0,
                            0, 0, layer, width, height, 1,
                            GL_BGRA, GL_UNSIGNED_INT_8_8_8_8_REV,
                            image.get_data())

    def bind(self, unit, u_texture):
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(GL_TEXTURE_2D_ARRAY, self.texture_handler)
        glUniform1i(u_texture, unit)

    @classmethod
    def bind_layer(cls, layer, u_layer):
        glUniform1i(u_layer, layer)

    @staticmethod
    def _get_texture_array_size(images):
        return (
            Texture2DArray._get_texture_array_width(images),
            Texture2DArray._get_texture_array_height(images))

    @staticmethod
    def _get_texture_array_width(images):
        widths = [image.width for image in images]
        first_width = widths[0]
        if all(filter(lambda w: w == first_width, widths)):
            return first_width
        raise ValueError('width of textures is not equal')

    @staticmethod
    def _get_texture_array_height(images):
        heights = [image.height for image in images]
        first_height = heights[0]
        if all(filter(lambda w: w == first_height, heights)):
            return first_height
        raise ValueError('height of textures is not equal')

    @staticmethod
    def _get_texture_array_data(images):
        image_bytes = b''.join([image.get_data() for image in images])
        return (c_ubyte * len(image_bytes))(*image_bytes)
