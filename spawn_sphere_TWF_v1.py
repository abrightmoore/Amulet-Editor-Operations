# @TheWorldFoundry

from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

from amulet.api.block import Block  # For working with Blocks
from amulet_nbt import *  # For working with block properties
from amulet.api.errors import ChunkDoesNotExist, ChunkLoadError


def spawn_sphere_TWF(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    print("spawn_sphere_TWF starting")

    radius = options["Radius"]

    rinner = radius - 1

    r2 = radius ** 2
    ri2 = rinner ** 2

    block_platform = "bedrock"  # the platform the blocks below are defined in
    block_version = (1, 17, 0)  # the version the blocks below are defined in
    block_inside = Block("minecraft", "air", {})  # This block will be at the centre
    block_edge = Block(
        "minecraft", "stained_glass", {"color": TAG_String("black")}
    )  # This block will be the main volume of the sphere

    replace_blocks = {
        "minecraft:air",
        "minecraft:lava",
        "minecraft:flowing_lava",
        "minecraft:water" "minecraft:flowing_water",
    }

    points = {}
    for box in selection:
        cx = (box.max_x + box.min_x) >> 1
        cy = (box.max_y + box.min_y) >> 1
        cz = (box.max_z + box.min_z) >> 1

        plots = {}

        for y in range(radius + 1):
            y2 = y ** 2
            for z in range(radius + 1):
                z2 = z ** 2
                for x in range(radius + 1):
                    x2 = x ** 2
                    dist = y2 + z2 + x2
                    block = None
                    if dist < r2:
                        if dist >= ri2:
                            block = block_edge
                        else:
                            block = block_inside
                    if block is not None:
                        points[(cx + x, cy + y, cz + z)] = block
                        points[(cx + x, cy + y, cz - z)] = block
                        points[(cx + x, cy - y, cz + z)] = block
                        points[(cx + x, cy - y, cz - z)] = block
                        points[(cx - x, cy + y, cz + z)] = block
                        points[(cx - x, cy + y, cz - z)] = block
                        points[(cx - x, cy - y, cz + z)] = block
                        points[(cx - x, cy - y, cz - z)] = block

    iter_count = len(points)
    count = 0
    for (x, y, z), block in points.items():
        try:
            src_block, block_e = world.get_version_block(
                x, y, z, dimension, (block_platform, block_version)
            )
            if src_block.namespaced_name in replace_blocks:
                world.set_version_block(
                    int(x),
                    int(y),
                    int(z),
                    dimension,
                    (block_platform, block_version),
                    block,
                )
        except ChunkLoadError:
            print(f"Unable to load chunk {x>>4}, {z>>4} at coordinates {x}, {z}")
        yield count / iter_count
        count += 1

    print("spawn_sphere_TWF ended")


operation_options = {
    "Radius": [
        "int",
        20,
    ]
}

export = {
    "name": "spawn_sphere_TWF (v1)",
    "operation": spawn_sphere_TWF,
    "options": operation_options,
}
