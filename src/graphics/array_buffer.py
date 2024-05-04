from pyglet.gl import *


class ArrayBuffer:
    def __init__(self, per_vertex):
        self.per_vertex = per_vertex

        self.data_count = 0
        self.data_size = 0
        self.vertex_count = 0

        self.vertex_buffer_handler = GLint()
        glGenBuffers(1, self.vertex_buffer_handler)

    def set_buffer(self, vertex_data):
        self.data_count = len(vertex_data)
        self.data_size = self.data_count * 4
        self.vertex_count = self.data_count // self.per_vertex

        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_handler)
        glBufferData(GL_ARRAY_BUFFER, self.data_size, vertex_data, GL_STATIC_DRAW)
