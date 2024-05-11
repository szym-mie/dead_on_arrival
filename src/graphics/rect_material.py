from src.graphics.mesh_material import MeshMaterial
from src.resource.default_resource_packs import base_pack


class RectMaterial(MeshMaterial):
    vertex_source_id = 'gl.rect_v'
    fragment_source_id = 'gl.rect_f'

    def __init__(self):
        vertex_source = base_pack.get(RectMaterial.vertex_source_id)
        fragment_source = base_pack.get(RectMaterial.fragment_source_id)

        super().__init__(vertex_source, fragment_source)

