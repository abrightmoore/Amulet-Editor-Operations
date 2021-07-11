# @TheWorldFoundry

from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

from amulet.api.block import Block  # For working with Blocks
from amulet.api.block_entity import BlockEntity
from amulet.api.errors import ChunkDoesNotExist, ChunkLoadError
from amulet_nbt import *  # For working with block properties
import random


def make_chunk_outline_TWF(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    """
    This method sets up a few block types by their block palette index, and randomly fills the selection
    with them. It relies on a couple of helper methods for finding the block index in the block palette
    and then using that to create the right block type in the world.
    @TheWorldFoundry 2021-06-26
    """
    print("make_chunk_outline Starting")

    block_platform = "bedrock"  # the platform the blocks below are defined in
    block_version = (1, 17, 0)  # the version the blocks below are defined in
    palette = [
        Block("minecraft", "wool", {"color": TAG_String("yellow")}),
        Block("minecraft", "wool", {"color": TAG_String("orange")}),
        Block("minecraft", "wool", {"color": TAG_String("black")}),
    ]

    chunk_locations = selection.chunk_locations()
    iter_count = len(chunk_locations)
    count = 0

    for cx, cz in selection.chunk_locations():
        try:
            py = 255
            for px in range(cx << 4, (cx << 4) + 16):
                pz = cz << 4
                block = random.choice(palette)
                world.set_version_block(
                    px, py, pz, dimension, (block_platform, block_version), block
                )
                pz = (cz << 4) + 16 - 1
                block = random.choice(palette)
                world.set_version_block(
                    px, py, pz, dimension, (block_platform, block_version), block
                )

            for pz in range(cz << 4, (cz << 4) + 16):
                px = cx << 4
                block = random.choice(palette)
                world.set_version_block(
                    px, py, pz, dimension, (block_platform, block_version), block
                )
                px = (cx << 4) + 16 - 1
                block = random.choice(palette)
                world.set_version_block(
                    px, py, pz, dimension, (block_platform, block_version), block
                )
        except ChunkDoesNotExist:
            print(f"Chunk not present {cx}, {cz}")
        except ChunkLoadError:
            print(f"Failed to load chunk {cx}, {cz} for some reason")

        count += 1
        yield count / iter_count


export = {"name": "make_chunk_outline (TWF v1)", "operation": make_chunk_outline_TWF}
