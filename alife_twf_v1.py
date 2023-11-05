#  @TheWorldFoundry
#     Randomly place blocks on the lowest layer of the selections
#     Then tick a cellular automation through each layer to produce a 3D sculpture

from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

from amulet.api.block import Block  # For working with Blocks
from amulet.api.block_entity import BlockEntity
from amulet_nbt import *  # For working with block properties

import math
import random
import json

def block_at(world, dimension, x, y, z):
    """Get the block at a given location in the world's version"""
    try:
        block, blockEntity = world.get_version_block(
            x, y, z, dimension, (world.level_wrapper.platform, world.level_wrapper.version)
        )
        return block, blockEntity
    except:
        return None, None

def print_field(field):
    for z in range(0, len(field)):
        row = field[z]
        output = ""
        for x in range(0, len(row)):
            output += str(row[x])
        print(output)

def calculate_next_step(field):
    new_field = []

    for z in range(len(field)):
        new_row = []
        for x in range(len(field[z])):
            #  print(x, len(field[z]))
            new_row.append(0)
            num_neighbours = 0
            for dz in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    px = x + dx
                    pz = z + dz
                    if (0 <= pz < len(field)-1) and (0 <= px < len(field[z])-1) and not (dx == 0 and dz == 0):
                        if field[pz][px] == 1:
                            num_neighbours += 1
            if ((num_neighbours < 2) or (num_neighbours > 3) and (field[z][x] == 1)):
                new_row[x] = 0
            elif ((num_neighbours == 3) and (field[z][x] != 1)):
                new_row[x] = 1
            else:
                new_row[x] = field[z][x]
        new_field.append(new_row)

    return new_field

def alife_twf(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    block_platform = "bedrock"  # the platform the blocks below are defined in
    block_version = (1, 20, 30)  # the version the blocks below are defined in
    blocks = [
        Block("minecraft", "air", {}),
        Block("minecraft", "iron_block", {}),
        Block("minecraft", "glowstone", {}),
        Block("minecraft", "wool", {"color": TAG_String("white")}),
        Block("minecraft", "wool", {"color": TAG_String("yellow")}),
        Block("minecraft", "wool", {"color": TAG_String("lime")}),
        Block("minecraft", "wool", {"color": TAG_String("magenta")}),
        Block("minecraft", "wool", {"color": TAG_String("pink")}),
        Block("minecraft", "wool", {"color": TAG_String("red")}),
        Block("minecraft", "wool", {"color": TAG_String("black")}),
        Block("minecraft", "wool", {"color": TAG_String("green")}),
        Block("minecraft", "wool", {"color": TAG_String("purple")}),
        Block("minecraft", "wool", {"color": TAG_String("brown")}),
        Block("minecraft", "wool", {"color": TAG_String("silver")}),
        Block("minecraft", "wool", {"color": TAG_String("gray")}),
    ]

    block_alive = blocks[1]  # This block will be at the centre
    block_dead = blocks[0]
    block_entity = None   #  Constant for non-containers

    points = {}
    for box in selection:
        width = box.max_x - box.min_x
        height = box.max_y - box.min_y
        depth = box.max_z - box.min_z

        #   Read in the lowest layer. Non-air blocks are "alive".
        field = []
        y = box.min_y
        for z in range(box.min_z, box.min_z+depth):
            row = []
            for x in range(box.min_x, box.min_x+width):
                block_here, block_entity_here = block_at(world, dimension, x, y, z)
                #  print(block_here)
                if block_here != None and block_here != blocks[0]:   #  Air
                    row.append(1)
                else:
                    row.append(0)
            field.append(row)

        #   Field is now populated, so I can work out what the rest of the layers should be
        


        while y < box.min_y+height-1:
            #  print(y)
            #  print("--------")
            #  print_field(field)
            field = calculate_next_step(field)
            y += 1

            #   Draw alive blocks to the world
            for z in range(len(field)):
                row = field[z]
                for x in range(len(row)):
                    if row[x] != 0:
                        world.set_version_block(
                            int(x+box.min_x),
                            int(y),
                            int(z+box.min_z),
                            dimension,
                            (block_platform, block_version),
                            blocks[1],   #   The populated block type
                            block_entity,
                        )
                    else:
                        world.set_version_block(
                            int(x+box.min_x),
                            int(y),
                            int(z+box.min_z),
                            dimension,
                            (block_platform, block_version),
                            blocks[0],   #   The populated block type
                            block_entity,
                        )
                        


export = {"name": "ALife TWF (v1)", "operation": alife_twf}










