from dataclasses import dataclass


@dataclass
class LevelTile:
    wall_id: int
    spawn_id: int
    is_solid: bool
    is_slab: bool
    z: float

    @classmethod
    def create_with_default_suppliers(cls, wall_id, spawn_id, is_solid_supplier, is_slab_supplier, z_supplier):
        is_solid = is_solid_supplier(wall_id)
        is_slab = is_slab_supplier(wall_id)
        z = z_supplier(wall_id)
        return cls(wall_id=wall_id, spawn_id=spawn_id, is_solid=is_solid, is_slab=is_slab, z=z)
