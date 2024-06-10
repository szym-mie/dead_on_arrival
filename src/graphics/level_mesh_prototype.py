from pyglet.gl import GL_TRIANGLES

from src.graphics.array_buffer import FloatArrayBuffer
from src.graphics.level_mesh_material import LevelMeshMaterial
from src.graphics.mesh_prototype import MeshPrototype
from src.graphics.texture_2d_array import Texture2DArray


class LevelMeshPrototype(MeshPrototype):
    @staticmethod
    def create_horizontal_faces(level):
        # 1---2
        # | \ |
        # 3---4
        #
        # horizontal
        # 1: [0, 0]
        # 2: [1, 0]
        # 3: [0, 1]
        # 4: [1, 1]
        #
        # 4, 2, 1, 1, 3, 4

        size = level.chunk_size
        position_array = []
        texcoord_array = []
        normal_array = []

        for lx, ly, level_chunk in level.chunks.with_position():
            nox = size * lx
            noy = size * ly
            pox = nox + 1
            poy = noy + 1
            for x, y, tile in level_chunk.tiles.with_position():
                tx = x + nox
                ty = y + noy
                prev_tile_y = level.get_tile_at(tx, ty - 1)
                next_tile_y = level.get_tile_at(tx, ty + 1)
                prev_tile_x = level.get_tile_at(tx - 1, ty)
                next_tile_x = level.get_tile_at(tx + 1, ty)
                corner_tile_pp = level.get_tile_at(tx - 1, ty - 1)
                corner_tile_np = level.get_tile_at(tx + 1, ty - 1)
                corner_tile_pn = level.get_tile_at(tx - 1, ty + 1)
                corner_tile_nn = level.get_tile_at(tx + 1, ty + 1)

                ptz_y = prev_tile_y.z if prev_tile_y is not None else 0
                ntz_y = next_tile_y.z if next_tile_y is not None else 0
                ptz_x = prev_tile_x.z if prev_tile_x is not None else 0
                ntz_x = next_tile_x.z if next_tile_x is not None else 0
                pptz = corner_tile_pp.z if corner_tile_pp is not None else 0
                nptz = corner_tile_np.z if corner_tile_np is not None else 0
                pntz = corner_tile_pn.z if corner_tile_pn is not None else 0
                nntz = corner_tile_nn.z if corner_tile_nn is not None else 0

                pnm_y = 0.8 if ptz_y > 0 else 1.0
                nnm_y = 0.8 if ntz_y > 0 else 1.0
                pnm_x = 0.8 if ptz_x > 0 else 1.0
                nnm_x = 0.8 if ntz_x > 0 else 1.0

                ppnm = 0.8 if pptz > 0 else 1.0
                npnm = 0.8 if nptz > 0 else 1.0
                pnnm = 0.8 if pntz > 0 else 1.0
                nnnm = 0.8 if nntz > 0 else 1.0

                z, wall_id = tile.z, tile.wall_id
                position_array.extend([
                    x + pox, y + poy, z, wall_id,
                    x + pox, y + noy, z, wall_id,
                    x + nox, y + noy, z, wall_id,
                    x + nox, y + noy, z, wall_id,
                    x + nox, y + poy, z, wall_id,
                    x + pox, y + poy, z, wall_id,
                ])
                texcoord_array.extend([
                    1.0, 1.0,
                    1.0, 0.0,
                    0.0, 0.0,
                    0.0, 0.0,
                    0.0, 1.0,
                    1.0, 1.0
                ])
                normal_array.extend([
                    0, 0, nnm_y * nnm_x * nnnm,
                    0, 0, pnm_y * nnm_x * npnm,
                    0, 0, pnm_y * pnm_x * ppnm,
                    0, 0, pnm_y * pnm_x * ppnm,
                    0, 0, nnm_y * pnm_x * pnnm,
                    0, 0, nnm_y * nnm_x * nnnm,
                ])

        return position_array, texcoord_array, normal_array

    @staticmethod
    def create_vertical_faces(level):
        # 1---2
        # | \ |
        # 3---4
        #
        # vertical
        # 1: [0, 1]
        # 2: [1, 1]
        # 3: [0, 0]
        # 4: [1, 0]
        #
        # 4, 2, 1, 1, 3, 4

        size = level.chunk_size
        position_array = []
        texcoord_array = []
        normal_array = []

        # face normal Y axis
        for lx, ly, level_chunk in level.chunks.with_position():
            nox = size * lx
            noy = size * ly
            pox = nox + 1
            for x, y, tile in level_chunk.tiles.with_position():
                tx = nox + x
                nty = noy + y
                pty = nty + 1
                z, wall_id = tile.z, tile.wall_id

                prev_tile = level.get_tile_at(tx, nty - 1)
                next_tile = level.get_tile_at(tx, nty + 1)

                if prev_tile is not None and prev_tile.z < tile.z:
                    # floor z
                    fz = prev_tile.z
                    position_array.extend([
                        x + pox, nty, fz, wall_id,
                        x + pox, nty, z, wall_id,
                        x + nox, nty, z, wall_id,
                        x + nox, nty, z, wall_id,
                        x + nox, nty, fz, wall_id,
                        x + pox, nty, fz, wall_id,
                    ])
                    texcoord_array.extend([
                        1, z,
                        1, fz,
                        0, fz,
                        0, fz,
                        0, z,
                        1, z
                    ])
                    normal_array.extend([
                        -1, 0, 0,
                        -1, 0, 0,
                        -1, 0, 0,
                        -1, 0, 0,
                        -1, 0, 0,
                        -1, 0, 0,
                    ])

                if next_tile is not None and next_tile.z < tile.z:
                    # floor z
                    fz = next_tile.z
                    position_array.extend([
                        x + pox, pty, fz, wall_id,
                        x + pox, pty, z, wall_id,
                        x + nox, pty, z, wall_id,
                        x + nox, pty, z, wall_id,
                        x + nox, pty, fz, wall_id,
                        x + pox, pty, fz, wall_id,
                    ])
                    texcoord_array.extend([
                        1, z,
                        1, fz,
                        0, fz,
                        0, fz,
                        0, z,
                        1, z
                    ])
                    normal_array.extend([
                        1, 0, 0,
                        1, 0, 0,
                        1, 0, 0,
                        1, 0, 0,
                        1, 0, 0,
                        1, 0, 0,
                    ])

        # face normal X axis
        for lx, ly, level_chunk in level.chunks.with_position():
            nox = size * lx
            noy = size * ly
            poy = noy + 1
            for x, y, tile in level_chunk.tiles.with_position():
                ntx = nox + x
                ptx = ntx + 1
                ty = noy + y
                z, wall_id = tile.z, tile.wall_id

                prev_tile = level.get_tile_at(ntx - 1, ty)
                next_tile = level.get_tile_at(ntx + 1, ty)

                if prev_tile is not None and prev_tile.z < tile.z:
                    # floor z
                    fz = prev_tile.z
                    position_array.extend([
                        ntx, y + poy, fz, wall_id,
                        ntx, y + poy, z, wall_id,
                        ntx, y + noy, z, wall_id,
                        ntx, y + noy, z, wall_id,
                        ntx, y + noy, fz, wall_id,
                        ntx, y + poy, fz, wall_id,
                    ])
                    texcoord_array.extend([
                        1, z,
                        1, fz,
                        0, fz,
                        0, fz,
                        0, z,
                        1, z
                    ])
                    normal_array.extend([
                        0, -1, 0,
                        0, -1, 0,
                        0, -1, 0,
                        0, -1, 0,
                        0, -1, 0,
                        0, -1, 0,
                    ])

                if next_tile is not None and next_tile.z < tile.z:
                    # floor z
                    fz = next_tile.z
                    position_array.extend([
                        ptx, y + poy, fz, wall_id,
                        ptx, y + poy, z, wall_id,
                        ptx, y + noy, z, wall_id,
                        ptx, y + noy, z, wall_id,
                        ptx, y + noy, fz, wall_id,
                        ptx, y + poy, fz, wall_id,
                    ])
                    texcoord_array.extend([
                        1, z,
                        1, fz,
                        0, fz,
                        0, fz,
                        0, z,
                        1, z
                    ])
                    normal_array.extend([
                        0, 1, 0,
                        0, 1, 0,
                        0, 1, 0,
                        0, 1, 0,
                        0, 1, 0,
                        0, 1, 0,
                    ])

        return position_array, texcoord_array, normal_array

    def __init__(self, level, diffuse_image_atlas):
        horizontal_faces = LevelMeshPrototype.create_horizontal_faces(level)
        vertical_faces = LevelMeshPrototype.create_vertical_faces(level)

        horizontal_faces_position, horizontal_faces_texcoord, horizontal_faces_normal = horizontal_faces
        vertical_faces_position, vertical_faces_texcoord, vertical_faces_normal = vertical_faces

        vertex_position_buffer = FloatArrayBuffer(horizontal_faces_position + vertical_faces_position, 4)
        vertex_texcoord_buffer = FloatArrayBuffer(horizontal_faces_texcoord + vertical_faces_texcoord, 2)
        vertex_normal_buffer = FloatArrayBuffer(horizontal_faces_normal + vertical_faces_normal, 3)
        material = LevelMeshMaterial()
        material.diffuse_texture = Texture2DArray(diffuse_image_atlas)

        super().__init__(GL_TRIANGLES,
                         vertex_position_buffer,
                         vertex_texcoord_buffer,
                         vertex_normal_buffer,
                         material)
