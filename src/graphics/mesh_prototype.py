from pyglet.gl import *

from src.graphics.mesh import Mesh


class MeshPrototype:
    def __init__(self,
                 draw_mode,
                 vertex_position_buffer,
                 vertex_texcoord_buffer,
                 vertex_normal_buffer,
                 material):
        self.draw_mode = draw_mode
        self.vertex_position_buffer = vertex_position_buffer
        self.vertex_texcoord_buffer = vertex_texcoord_buffer
        self.vertex_normal_buffer = vertex_normal_buffer
        self.material = material

        self.meshes = []

    def create_mesh(self, position, rotation, scale):
        mesh = Mesh(position, rotation, scale, self)
        self.meshes.append(mesh)
        return mesh

    def remove_mesh(self, mesh):
        self.meshes.remove(mesh)

    def pre_bind(self, camera):
        self.material.pre_bind(camera)
        self.vertex_position_buffer.bind(self.material.a_vertex_position)
        self.vertex_texcoord_buffer.bind(self.material.a_vertex_texcoord)
        self.vertex_normal_buffer.bind(self.material.a_vertex_normal)

    def draw(self, camera):
        self.pre_bind(camera)
        for mesh in self.meshes:
            mesh.bind()
            glDrawArrays(self.draw_mode, 0, self.vertex_position_buffer.vertex_count)

    @staticmethod
    def _create_buffer():
        buffer = GLuint()
        glGenBuffers(1, buffer)
        return buffer

    @staticmethod
    def _create_texture():
        texture = GLuint()
        glGenTextures(1, texture)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        return texture
