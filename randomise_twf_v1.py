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

class WorldContext:
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


class OperationControl:
    def __init__(self, selection):
        self.selection = selection
        self.progress = 0.0
        self.stage = 0
        self.num_selections = len(selection)
        self.operation_length = 1.0/float(self.num_selections)
        self.yield_quantum = 0.0
        self.total_yield_by_box_sizes = 0  #  This yield strategy is used when we're iterating over all the points in all the boxes so we can work out how big the job is.
        self.calculate_full_yield()
        if(export != None):  #  This is set at bottom, scope is on parent script
            print("Initialised Operation: "+export["name"])
            
            
    def calculate_full_yield(self):
        total = 0
        if self.selection != None:
            for box in self.selection:
                width = box.max_x - box.min_x
                height = box.max_y - box.min_y
                depth = box.max_z - box.min_z
                total += width * height * depth
        self.total_yield_by_box_sizes = total
        
    def set_yield_quantum(self):
        self.yield_quantum = self.operation_length/float(self.selection[self.stage].max_y - self.selection[self.stage].min_y)
        
    def get_next_box(self):
        if self.stage < len(self.selection):
            print("Processing box "+str(self.stage+1)+" of "+str(len(self.selection)))
            self.stage += 1
            return self.selection[self.stage-1]
        return None

    def get_current_box(self):
        if self.stage < len(self.selection):
            self.set_yield_quantum()
            return self.selection[self.stage]
        else:
            return None

    def show_progress(self, val):
        self.progress = float(self.stage)*self.operation_length + float(val-self.get_current_box().min_y)*self.yield_quantum        
        #  print("Yielding at "+str(self.progress))
        return self.progress

    def show_progress_by_blocks_processed(self, val):
        if self.total_yield_by_box_sizes > 0 and val <= self.total_yield_by_box_sizes:
            self.progress = float(val)/float(self.total_yield_by_box_sizes)
        else:
            self.progress = 0.1 + random.random() *0.9  # Show activity even if we can't work out what it is
        #  print("Yielding at "+str(self.progress))
        return self.progress


def perform(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    world_context = WorldContext(world, dimension, [ Block("minecraft", "air", {}), Block("minecraft", "iron_block", {}) ])

    block_alive = world_context.block_palette[1]  # This block will be at the centre
    block_dead = world_context.block_palette[0]
    block_entity = None   #  Constant for non-containers

    op_control = OperationControl(selection)   #  Progress bar stats
    blocks_processed = 0   #  Progress bar stats
    while op_control.get_current_box():   #  Progress bar stats
        box = op_control.get_current_box()   #  Progress bar stats
        
        chance = random.random()*0.5+0.01
    
        for y in range(box.min_y, box.max_y):
            for z in range(box.min_z, box.max_z):
                for x in range(box.min_x, box.max_x):
                    blocks_processed += 1    #  Progress bar stats
                    block = block_alive
                    if random.random() > chance:
                        block = block_dead

                    world_context.set_block_at(
                        int(x),
                        int(y),
                        int(z),
                        block,   #   The populated block type
                        block_entity,
                    )
                yield op_control.show_progress_by_blocks_processed(blocks_processed)   #  Progress bar stats
        box = op_control.get_next_box()   #  Progress bar stats

export = {"name": "Randomise TWF (v1)", "operation": perform}










