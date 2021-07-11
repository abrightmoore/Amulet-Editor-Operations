# @TheWorldFoundry

from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

from amulet.api.level import ImmutableStructure


def mark_box_dirty(world, dimension, box):
    for cx, cz in box.chunk_locations():  # Mark the edits as dirty
        chunk = world.get_chunk(cx, cz, dimension)
        chunk.changed = True


def clone_to_sky_TWF(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    """
    This method repeats the selection, vertically tiling, until the height limit is reached
    @TheWorldFoundry 2021-06-26
    """

    print("clone_to_sky Starting")

    for box in selection:
        height = box.max_y - box.min_y
        cx = (box.max_x + box.min_x) >> 1
        cy = ((box.max_y + box.min_y) >> 1) + height  # Paste is from-centre
        cz = (box.max_z + box.min_z) >> 1
        structure = ImmutableStructure.from_level(world, SelectionGroup(box), dimension)
        print(structure.bounds(dimension))

        while cy + height < 256:  # How to get the max height of the chunks here?
            print(cy)
            world.paste(
                structure,
                structure.dimensions[0],
                SelectionGroup(box),
                dimension,
                (cx, cy, cz),
                [1.0, 1.0, 1.0],
                [0.0, 0.0, 0.0],
                True,
                False,
                [],
                False,
            )

            cy += height

        mark_box_dirty(world, dimension, box)


export = {"name": "clone_to_sky (TWF v1)", "operation": clone_to_sky_TWF}
