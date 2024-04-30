from pyglet.gl import *
from pyglet.graphics.shader import ShaderProgram, Shader


class Rect:
    vertices = [1, 1, -1, 1, 1, -1, -1, -1]
    data_count = len(vertices)
    data_size = data_count * 4
    vertex_count = data_count // 2
    vertex_array = (GLfloat * data_count)(*vertices)
    vertex_buffer = GLuint()

    shader = None

    def __init__(self, texture):
        self.position_x = 0.0
        self.position_y = 0.0
        self.position_z = 0.0
        self.rotation = 0.0
        self.scale = 1

        self.texture = texture

        glGenBuffers(1, Rect.vertex_buffer)
        glBindBuffer(GL_ARRAY_BUFFER, Rect.vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, Rect.data_size, Rect.vertex_array, GL_STATIC_DRAW)

    @staticmethod
    def update_shader(vertex_source, fragment_source):
        Rect.shader = ShaderProgram(
            Shader(vertex_source, 'vertex'),
            Shader(fragment_source, 'fragment')
        )

    def draw(self, projection):
        u_position = Rect.shader.uniforms['position']['location']
        u_rotation = None
        u_scale = None
        u_projection = None
        u_diffuse_sampler = None
        a_vertex = None

        glUniform3f(u_position, self.position_x, self.position_y, self.position_z)
        glUniform1f(u_rotation, self.rotation)
        glUniform1f(u_scale, self.scale)
        glUniformMatrix4fv(u_projection, projection)

        glBindTexture(GL_TEXTURE0, self.texture)
        glUniform1i(u_diffuse_sampler, GL_TEXTURE0)

        glEnableVertexAttribArray(a_vertex)
        glBindBuffer(GL_ARRAY_BUFFER, Rect.vertex_buffer)
        glVertexAttribPointer(a_vertex, 2, GL_FLOAT, GL_FALSE, 0, 0)

        glDrawArrays(GL_TRIANGLE_STRIP, 0, Rect.vertex_count)
