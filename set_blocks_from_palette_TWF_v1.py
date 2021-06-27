# @TheWorldFoundry

from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

from amulet.api.block import Block  #  For working with Blocks
from amulet_nbt import TAG_String, TAG_Int, TAG_Byte  #  For working with block properties
import random

def get_native_block_by_name(world, namespace, name, properties):
    block, blockEntity, isBlock = world.translation_manager.get_version( world.level_wrapper.platform, world.level_wrapper.version).block.to_universal(Block(namespace, name, properties))
    return (block, blockEntity, isBlock)

def set_blocks_from_palette_TWF(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    '''
        This method sets up a few block types by their block palette index, and randomly fills the selection
        with them. It relies on a couple of helper methods for finding the block index in the block palette
        and then using that to create the right block type in the world.
        @TheWorldFoundry 2021-06-26
    '''
    iter_count = len(list(world.get_chunk_slice_box(dimension, selection)))
    count = 0
    
    print ("set_blocks_from_palette Starting")

    palette = [
                get_native_block_by_name(world, "minecraft", "wool", { "color": TAG_String("white") }),
                get_native_block_by_name(world, "minecraft", "wool", { "color": TAG_String("orange") }),
                get_native_block_by_name(world, "minecraft", "wool", { "color": TAG_String("magenta") }),
                get_native_block_by_name(world, "minecraft", "wool", { "color": TAG_String("light blue") }),
                get_native_block_by_name(world, "minecraft", "wool", { "color": TAG_String("yellow") }),
                get_native_block_by_name(world, "minecraft", "wool", { "color": TAG_String("lime") }),
                get_native_block_by_name(world, "minecraft", "wool", { "color": TAG_String("pink") }),
                get_native_block_by_name(world, "minecraft", "wool", { "color": TAG_String("gray") }),
                get_native_block_by_name(world, "minecraft", "wool", { "color": TAG_String("light gray") }),
                get_native_block_by_name(world, "minecraft", "wool", { "color": TAG_String("cyan") }),
                get_native_block_by_name(world, "minecraft", "wool", { "color": TAG_String("purple") }),
                get_native_block_by_name(world, "minecraft", "wool", { "color": TAG_String("blue") }),
                get_native_block_by_name(world, "minecraft", "wool", { "color": TAG_String("brown") }),
                get_native_block_by_name(world, "minecraft", "wool", { "color": TAG_String("green") }),
                get_native_block_by_name(world, "minecraft", "wool", { "color": TAG_String("red") }),
                get_native_block_by_name(world, "minecraft", "wool", { "color": TAG_String("black") }),
                get_native_block_by_name(world, "minecraft", "stone", {}),
                get_native_block_by_name(world, "minecraft", "stone", {"stone_type": TAG_String("diorite")}),
                get_native_block_by_name(world, "minecraft", "stone", {"stone_type": TAG_String("diorite_smooth")})

            ]


    for box in selection:
        for px, py, pz in box:
            block, blockEntity, isBlock = random.choice(palette)
            print (block, blockEntity, isBlock)
            world.set_version_block(px, py, pz, dimension, (world.level_wrapper.platform, world.level_wrapper.version), block, blockEntity)
        
        count += 1
        yield count / iter_count
    


export = {
    "name": "set_blocks_from_palette (TWF v1)",
    "operation": set_blocks_from_palette_TWF
}
