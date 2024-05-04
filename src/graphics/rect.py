from pyglet.gl import *
from pyglet.graphics.shader import ShaderProgram, Shader


class Rect:
    vertices = [1, 1, -1, 1, 1, -1, -1, -1]
    data_count = len(vertices)
    data_size = data_count * 4
    vertex_count = data_count // 2
    vertex_array = (GLfloat * data_count)(*vertices)
    vertex_buffer = GLuint()
    texture = GLuint()

    shader = None

    def __init__(self, texture):
        self.position_x = 0.0
        self.position_y = 0.0
        self.position_z = 0.0
        self.rotation = 0.0
        self.scale = 1

        self.texture = texture
        self.texture_ref = None

        glGenBuffers(1, Rect.vertex_buffer)
        glBindBuffer(GL_ARRAY_BUFFER, Rect.vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, Rect.data_size, Rect.vertex_array, GL_STATIC_DRAW)

        glGenTextures(1, Rect.texture)

    @staticmethod
    def update_shader(vertex_source, fragment_source):
        Rect.shader = ShaderProgram(
            Shader(vertex_source, 'vertex'),
            Shader(fragment_source, 'fragment')
        )

    def draw(self, projection):
        Rect.shader.bind()
        print(Rect.shader.uniforms)
        u_position = Rect.shader.uniforms['position']['location']
        u_rotation = Rect.shader.uniforms['rotation']['location']
        u_scale = Rect.shader.uniforms['scale']['location']
        u_projection = Rect.shader.uniforms['projection']['location']
        u_diffuse_texture = Rect.shader.uniforms['diffuse_texture']['location']
        a_vertex = Rect.shader.attributes['vertex']['location']

        glUniform3f(u_position, GLfloat(self.position_x),  GLfloat(self.position_y),  GLfloat(self.position_z))
        glUniform1f(u_rotation, GLfloat(self.rotation))
        glUniform1f(u_scale, GLfloat(self.scale))
        projection_carray = (GLfloat * 16)(*projection)
        glUniformMatrix4fv(u_projection, 1, GL_FALSE, projection_carray)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, Rect.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.texture.width, self.texture.height, 0, GL_BGRA, GL_UNSIGNED_BYTE, self.texture.get_data())
        glActiveTexture(GL_TEXTURE0)
        glUniform1i(u_diffuse_texture, 0)

        glEnableVertexAttribArray(a_vertex)
        glBindBuffer(GL_ARRAY_BUFFER, Rect.vertex_buffer)
        glVertexAttribPointer(a_vertex, 2, GL_FLOAT, GL_FALSE, 0, 0)

        glDrawArrays(GL_TRIANGLE_STRIP, 0, Rect.vertex_count)
