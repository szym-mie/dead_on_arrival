from pyglet.gl import GL_TRIANGLE_STRIP

from src.graphics.array_buffer import FloatArrayBuffer
from src.graphics.mesh_prototype import MeshPrototype
from src.graphics.texture import Texture
from src.resource.default_resource_packs import base_pack


class RectPrototype(MeshPrototype):
    vertex_source_id = 'gl.rect_v'
    fragment_source_id = 'gl.rect_f'
    vertices = [1, 1, -1, 1, 1, -1, -1, -1]

    def __init__(self, diffuse_image):
        diffuse_texture = Texture(diffuse_image)
        vertex_source = base_pack.get(RectPrototype.vertex_source_id)
        fragment_source = base_pack.get(RectPrototype.fragment_source_id)
        vertex_buffer = FloatArrayBuffer(RectPrototype.vertices, 2)

        super().__init__(GL_TRIANGLE_STRIP,
                         vertex_source, fragment_source,
                         vertex_buffer,
                         diffuse_texture)
