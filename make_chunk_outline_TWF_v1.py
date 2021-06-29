# @TheWorldFoundry

from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

from amulet.api.block import Block  #  For working with Blocks
from amulet.api.block_entity import BlockEntity
from amulet_nbt import *  #  For working with block properties
import random

def get_native_block_by_name(world, namespace, name, properties):
    block, blockEntity, isPartial = world.translation_manager.get_version( world.level_wrapper.platform, world.level_wrapper.version).block.to_universal(Block(namespace, name, properties))
    return (block, blockEntity, isPartial)

def make_chunk_outline_TWF(
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
    
    print ("make_chunk_outline Starting")

    palette = [
                get_native_block_by_name(world, "minecraft", "wool", { "color": TAG_String("yellow") }),

                get_native_block_by_name(world, "minecraft", "wool", { "color": TAG_String("orange") }),
                get_native_block_by_name(world, "minecraft", "wool", { "color": TAG_String("black") }),
            ]


    for box in selection:
        for cx, cz in box.chunk_locations():
            chunk = world.get_chunk(cx, cz, dimension)  
            py = 255
            
            for px in range(cx<<4, (cx<<4)+16):
                    pz = cz<<4
                    block, blockEntity, isPartial = random.choice(palette)
                    world.set_version_block(px, py,  pz, dimension, (world.level_wrapper.platform, world.level_wrapper.version), block, blockEntity)
                    pz = (cz<<4)+16-1
                    block, blockEntity, isPartial = random.choice(palette)
                    world.set_version_block(px, py,  pz, dimension, (world.level_wrapper.platform, world.level_wrapper.version), block, blockEntity)
                    
            for pz in range(cz<<4, (cz<<4)+16):
                    px = cx<<4
                    block, blockEntity, isPartial = random.choice(palette)
                    world.set_version_block(px, py,  pz, dimension, (world.level_wrapper.platform, world.level_wrapper.version), block, blockEntity)
                    px = (cx<<4)+16-1
                    block, blockEntity, isPartial = random.choice(palette)
                    world.set_version_block(px, py,  pz, dimension, (world.level_wrapper.platform, world.level_wrapper.version), block, blockEntity)
    
        count += 1
        yield count / iter_count
    


export = {
    "name": "make_chunk_outline (TWF v1)",
    "operation": make_chunk_outline_TWF
}
