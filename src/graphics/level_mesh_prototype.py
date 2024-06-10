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
                    0, 0, 1,
                    0, 0, 1,
                    0, 0, 1,
                    0, 0, 1,
                    0, 0, 1,
                    0, 0, 1,
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
