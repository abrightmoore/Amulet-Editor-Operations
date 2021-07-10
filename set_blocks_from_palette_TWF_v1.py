# @TheWorldFoundry

from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

from amulet.api.block import Block  # For working with Blocks
from amulet_nbt import (
    TAG_String,
    TAG_Int,
    TAG_Byte,
)  # For working with block properties
import random


def set_blocks_from_palette_TWF(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    """
    This method sets up a few block types by their block palette index, and randomly fills the selection
    with them. It relies on a couple of helper methods for finding the block index in the block palette
    and then using that to create the right block type in the world.
    @TheWorldFoundry 2021-06-26
    """
    iter_count = len(list(world.get_chunk_slice_box(dimension, selection)))
    count = 0

    print("set_blocks_from_palette Starting")

    block_platform = "bedrock"  # the platform the blocks below are defined in
    block_version = (1, 17, 0)  # the version the blocks below are defined in
    palette = [
        Block("minecraft", "wool", {"color": TAG_String("white")}),
        Block("minecraft", "wool", {"color": TAG_String("orange")}),
        Block("minecraft", "wool", {"color": TAG_String("magenta")}),
        Block("minecraft", "wool", {"color": TAG_String("light blue")}),
        Block("minecraft", "wool", {"color": TAG_String("yellow")}),
        Block("minecraft", "wool", {"color": TAG_String("lime")}),
        Block("minecraft", "wool", {"color": TAG_String("pink")}),
        Block("minecraft", "wool", {"color": TAG_String("gray")}),
        Block("minecraft", "wool", {"color": TAG_String("light gray")}),
        Block("minecraft", "wool", {"color": TAG_String("cyan")}),
        Block("minecraft", "wool", {"color": TAG_String("purple")}),
        Block("minecraft", "wool", {"color": TAG_String("blue")}),
        Block("minecraft", "wool", {"color": TAG_String("brown")}),
        Block("minecraft", "wool", {"color": TAG_String("green")}),
        Block("minecraft", "wool", {"color": TAG_String("red")}),
        Block("minecraft", "wool", {"color": TAG_String("black")}),
        Block("minecraft", "stone", {}),
        Block("minecraft", "stone", {"stone_type": TAG_String("diorite")}),
        Block("minecraft", "stone", {"stone_type": TAG_String("diorite_smooth")}),
    ]

    for box in selection:
        for px, py, pz in box:
            block = random.choice(palette)
            print(block)
            world.set_version_block(
                px, py, pz, dimension, (block_platform, block_version), block
            )

        count += 1
        yield count / iter_count


export = {
    "name": "set_blocks_from_palette (TWF v1)",
    "operation": set_blocks_from_palette_TWF,
}
