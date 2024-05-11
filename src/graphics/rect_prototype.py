from pyglet.gl import GL_TRIANGLE_STRIP

from src.graphics.array_buffer import FloatArrayBuffer
from src.graphics.mesh_prototype import MeshPrototype
from src.graphics.rect_material import RectMaterial
from src.graphics.texture import Texture


class RectPrototype(MeshPrototype):
    vertices = [1, 1, -1, 1, 1, -1, -1, -1]

    def __init__(self, diffuse_image):
        vertex_buffer = FloatArrayBuffer(RectPrototype.vertices, 2)
        material = RectMaterial()
        material.diffuse_texture = Texture(diffuse_image)

        super().__init__(GL_TRIANGLE_STRIP,
                         vertex_buffer,
                         material)
