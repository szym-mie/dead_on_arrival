from pyglet.gl import *


class Texture:
    def __init__(self, image):
        self.texture_handler = GLuint()
        glGenTextures(1, self.texture_handler)
        glBindTexture(GL_TEXTURE_2D, self.texture_handler)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        self.set_texture(image)

    def set_texture(self, image):
        glBindTexture(GL_TEXTURE_2D, self.texture_handler)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                     image.width, image.height, 0,
                     GL_BGRA, GL_UNSIGNED_BYTE,
                     image.get_data())
        glGenerateMipmap(GL_TEXTURE_2D)

    def bind(self, unit, u_texture):
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(GL_TEXTURE_2D, self.texture_handler)
        glUniform1i(u_texture, unit)
