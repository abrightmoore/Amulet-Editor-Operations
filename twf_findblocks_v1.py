#   @TheWorldFoundry

#   Find Command Blocks, requested by kqlamari
#   20240329

BLOCKS_TO_FIND = [
    "minecraft:command_block",
    "minecraft:chain_command_block",
    "minecraft:repeating_command_block",
]



#  Amulet Editor standard includes for an operation
from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

from amulet.api.block import Block  # For working with Blocks
from amulet.api.block_entity import BlockEntity
from amulet_nbt import *  # For working with block properties

#  Useful includes for voxel editing
import math
from math import pi, cos, sin
from random import randint
import json

OPERATION_NAME = "FINDBLOCKS TWF 2024 (v1)"

#  This is a static stub to be replaced with the Amulet UI framework
inputs = (
        (OPERATION_NAME, "label"),
        ("adrian@TheWorldFoundry.com", "label"),
        ("http://theworldfoundry.com", "label")
)

#  Shim to port MCEdit inputs to options
options_from_inputs = {}    #  Shim to port MCEdit inputs to options
for part in inputs: #  Shim to port MCEdit inputs to options
    options_from_inputs[part[0]] = part[1]  #  Shim to port MCEdit inputs to options

class WorldContext:
    blocks = [
        (Block("minecraft", "air", {}),None),
        (Block("twf", "girder_panel", {}),None),
        (Block("minecraft", "sea_lantern", {}),None),
        (Block("minecraft", "iron_block", {}),None),
        (Block("minecraft", "glowstone", {}),None),
        (Block("minecraft", "white_wool", {}),None),
        (Block("minecraft", "yellow_wool", {}),None),
        (Block("minecraft", "lime_wool", {}),None),
        (Block("minecraft", "magenta_wool", {}),None),
        (Block("minecraft", "pink_wool", {}),None),
        (Block("minecraft", "red_wool", {}),None),
        (Block("minecraft", "black_wool", {}),None),
        (Block("minecraft", "green_wool", {}),None),
        (Block("minecraft", "purple_wool", {}),None),
        (Block("minecraft", "brown_wool", {}),None),
        (Block("minecraft", "silver_wool", {}),None),
        (Block("minecraft", "gray_wool", {}),None)
    ]

    def __init__(self, world_context, dimension, block_palette):
        self.world = world_context
        self.dimension = dimension
        self.block_palette = block_palette
        if self.block_palette == None:
            self.block_palette = self.blocks
        
    def block_at(self, x, y, z):
        """Get the block at a given location in the world's version"""
        try:
            block, blockEntity = self.world.get_version_block(
                x, y, z, self.dimension, (self.world.level_wrapper.platform, self.world.level_wrapper.version)
            )
            return block, blockEntity
        except:
            return None, None

    def set_block(self, x, y, z, block):
        self.set_block_at(x, y, z, block[0], block[1])

    def set_block_at(self, x, y, z, block, block_entity):
        self.world.set_version_block(
            int(x),
            int(y),
            int(z),
            self.dimension,
            (self.world.level_wrapper.platform, self.world.level_wrapper.version),
            block,
            block_entity
        )
        print("set_block_at end")

    def get_box_size(self, box):
        return (box.max_x - box.min_x, box.max_y - box.min_y, box.max_z - box.min_z)
        

def findblocks(world, box, options):
    print(OPERATION_NAME+" starting")
    
    for x in range(box.min_x,box.max_x):
        for z in range(box.min_z,box.max_z):
            for y in range(box.min_y,box.max_y):
                block, blockentity = world.block_at(x, y, z)
                if block is not None:
                    #  print(str(block))
                    for btf in BLOCKS_TO_FIND:
                        if btf in str(block):
                            print("/setblock "+str(x)+" "+str(y)+" "+str(z)+" "+str(block))
                        

    print(OPERATION_NAME+" finished")
    

def perform_twf(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    for box in selection:
        findblocks(WorldContext(world, dimension, None), box, options_from_inputs)

export = {"name": OPERATION_NAME, "operation": perform_twf}    