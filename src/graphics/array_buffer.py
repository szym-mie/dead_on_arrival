from ctypes import c_void_p

from pyglet.gl import *


class FloatArrayBuffer:
    def __init__(self, init_array=None, per_vertex=3):
        self.per_vertex = per_vertex

        self.data_count = 0
        self.data_size = 0
        self.vertex_count = 0

        self.vertex_buffer_handle = GLuint()
        glGenBuffers(1, self.vertex_buffer_handle)
        if init_array is not None:
            self.set_buffer(init_array)

    def set_buffer(self, vertex_data):
        self.data_count = len(vertex_data)
        self.data_size = self.data_count * 4
        self.vertex_count = self.data_count // self.per_vertex
        vertex_array = (GLfloat * self.data_count)(*vertex_data)

        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_handle)
        glBufferData(GL_ARRAY_BUFFER, self.data_size, vertex_array, GL_STATIC_DRAW)

    def bind(self, a_vertex):
        if a_vertex == -1:
            return
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_handle)
        glEnableVertexAttribArray(a_vertex)
        glVertexAttribPointer(a_vertex,
                              self.per_vertex,
                              GL_FLOAT, GL_FALSE,
                              0, c_void_p(0))
