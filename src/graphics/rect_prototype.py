from pyglet.gl import GL_TRIANGLE_STRIP

from src.graphics.array_buffer import FloatArrayBuffer
from src.graphics.mesh_prototype import MeshPrototype
from src.graphics.rect_material import RectMaterial
from src.graphics.texture_2d import Texture2D


class RectPrototype(MeshPrototype):
    position_vertices = [1,  1, -1,  1,  1, -1, -1, -1]
    texcoord_vertices = [1,  1,  0,  1,  1,  0,  0,  0]
    normal_vertices = [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]

    def __init__(self, diffuse_image):
        vertex_position_buffer = FloatArrayBuffer(RectPrototype.position_vertices, 2)
        vertex_texcoord_buffer = FloatArrayBuffer(RectPrototype.texcoord_vertices, 2)
        vertex_normal_buffer = FloatArrayBuffer(RectPrototype.normal_vertices, 3)
        material = RectMaterial()
        material.diffuse_texture = Texture2D(diffuse_image)

        super().__init__(GL_TRIANGLE_STRIP,
                         vertex_position_buffer,
                         vertex_texcoord_buffer,
                         vertex_normal_buffer,
                         material)
