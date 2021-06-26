# @TheWorldFoundry

from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

from amulet.api.block import Block  #  For working with Blocks
from amulet_nbt import TAG_String, TAG_Int, TAG_Byte  #  For working with block properties
import random

def getBlockIndex(world, namespace, base_name, properties):
    '''
        This method tries to find the block index for the named block in the current loaded world palette
        Warning: if the block does NOT exist, this may return a new id which will be meaningless at runtime
        @TheWorldFoundry 2021-06-26
    '''
    loaded_level_version = world.level_wrapper.version
    loaded_level_platform = world.level_wrapper.platform
    
    block = Block(namespace, base_name, properties)
    universal_block = world.translation_manager.get_version( loaded_level_platform, loaded_level_version).block.to_universal(block)[0]
    universal__block_index = world.block_palette.get_add_block(universal_block)
    return universal__block_index

def set_block( world, dimension, pos, block_index ):
    '''
        This method places the requested block (by index value) into the world at the specified position
        if the chunk already exists. It's your job to sort out creating the chunks before doing block setting.
        @TheWorldFoundry 2021-06-26
    '''
    x, y, z = pos
    cx = x >> 4  #  Chunks are 16 blocks wide. Shifting 4 bits divides by 16 
    cz = z >> 4
    theChunk = world.get_chunk(cx, cz, dimension)
    dx = x-(cx<<4) # Desired position in the chunk. This could also be bitwise ANDed.
    dz = z-(cz<<4)
    theChunk.blocks[dx,y,dz] = block_index
    theChunk.changed = True

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
                getBlockIndex(world, "minecraft", "wool", { "color": TAG_String("white") }),
                getBlockIndex(world, "minecraft", "wool", { "color": TAG_String("orange") }),
                getBlockIndex(world, "minecraft", "wool", { "color": TAG_String("magenta") }),
                getBlockIndex(world, "minecraft", "wool", { "color": TAG_String("light blue") }),
                getBlockIndex(world, "minecraft", "wool", { "color": TAG_String("yellow") }),
                getBlockIndex(world, "minecraft", "wool", { "color": TAG_String("lime") }),
                getBlockIndex(world, "minecraft", "wool", { "color": TAG_String("pink") }),
                getBlockIndex(world, "minecraft", "wool", { "color": TAG_String("gray") }),
                getBlockIndex(world, "minecraft", "wool", { "color": TAG_String("light gray") }),
                getBlockIndex(world, "minecraft", "wool", { "color": TAG_String("cyan") }),
                getBlockIndex(world, "minecraft", "wool", { "color": TAG_String("purple") }),
                getBlockIndex(world, "minecraft", "wool", { "color": TAG_String("blue") }),
                getBlockIndex(world, "minecraft", "wool", { "color": TAG_String("brown") }),
                getBlockIndex(world, "minecraft", "wool", { "color": TAG_String("green") }),
                getBlockIndex(world, "minecraft", "wool", { "color": TAG_String("red") }),
                getBlockIndex(world, "minecraft", "wool", { "color": TAG_String("black") }),
                
                getBlockIndex(world, "minecraft", "stone", {}),
                getBlockIndex(world, "minecraft", "diorite", {}),
                getBlockIndex(world, "minecraft", "diorite", { "polished": TAG_Byte(1) })
            ]


    for box in selection:
        for pos in box:
            set_block( world, dimension, pos, random.choice(palette))
        
        count += 1
        yield count / iter_count
    


export = {
    "name": "set_blocks_from_palette (TWF v1)",
    "operation": set_blocks_from_palette_TWF
}
