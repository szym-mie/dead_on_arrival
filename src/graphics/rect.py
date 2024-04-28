from pyglet.gl import *


class Rect:
    vertices = [1, 1, -1, 1, 1, -1, -1, -1]
    data_count = len(vertices)
    data_size = data_count * 4
    vertex_count = data_count // 2
    vertex_array = (GLfloat * data_count)(*vertices)
    vertex_buffer = None

    def __init__(self, texture):
        self.position_x = 0
        self.position_y = 0
        self.position_z = 0
        self.azimuth = 0

        self.texture = texture

        glGenBuffers(1, Rect.vertex_buffer)
        glBindBuffer(GL_ARRAY_BUFFER, Rect.vertex_buffer)
        glBufferData(Rect.vertex_buffer, Rect.data_size, Rect.vertex_array, GL_STATIC_DRAW)

    def draw(self):
        glBindTexture(GL_TEXTURE0, self.texture)
        glBindTexture(GL_ARRAY_BUFFER, Rect.vertex_buffer)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, Rect.vertex_count)
