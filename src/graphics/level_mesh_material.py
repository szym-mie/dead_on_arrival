from src.graphics.mesh_material import MeshMaterial
from src.resource.default_resource_packs import base_pack


class LevelMeshMaterial(MeshMaterial):
    vertex_source_id = 'gl.level_v'
    fragment_source_id = 'gl.level_f'

    def __init__(self):
        vertex_source = base_pack.get(LevelMeshMaterial.vertex_source_id)
        fragment_source = base_pack.get(LevelMeshMaterial.fragment_source_id)

        super().__init__(vertex_source, fragment_source)

    def pre_bind(self, camera):
        self.use_program()
        camera.bind_to(self.u_projection, self.u_view)
        MeshMaterial.try_bind_texture(self.diffuse_texture, 3, self.u_diffuse_texture)
        # MeshMaterial.try_bind_texture(self.normal_texture, 1, self.u_normal_texture)
        # MeshMaterial.try_bind_texture(self.emission_texture, 2, self.u_emission_texture)
