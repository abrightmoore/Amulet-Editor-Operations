#  @TheWorldFoundry

'''
    Attempt to place blocks of a certain type around the landscape upon blocks that are suitable for placement.
'''

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
    saplings = [
        Block("minecraft", "sapling", { "age_bit": TAG_Byte(1), "sapling_type": TAG_String("oak")}),
        Block("minecraft", "sapling", { "age_bit": TAG_Byte(1), "sapling_type": TAG_String("spruce")}),
        Block("minecraft", "sapling", { "age_bit": TAG_Byte(1), "sapling_type": TAG_String("birch")}),
        Block("minecraft", "sapling", { "age_bit": TAG_Byte(1), "sapling_type": TAG_String("jungle")}),
        Block("minecraft", "sapling", { "age_bit": TAG_Byte(1), "sapling_type": TAG_String("acacia")}),
        Block("minecraft", "sapling", { "age_bit": TAG_Byte(1), "sapling_type": TAG_String("dark_oak")}),
        Block("minecraft", "bamboo_sapling", { "age_bit": TAG_Byte(1)}),
        Block("minecraft", "cherry_sapling", { "age_bit": TAG_Byte(1)}),    
    ]
    
    blocks = [
        Block("minecraft", "air", {}),
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
        Block("minecraft", "dirt", {})
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
    world_context = WorldContext(world, dimension, WorldContext.saplings)

    blocks_plantable =  [ Block("minecraft", "dirt", {}),
                          Block("minecraft", "grass", {})
                        ]

    op_control = OperationControl(selection)   #  Progress bar stats
    blocks_processed = 0   #  Progress bar stats

    while op_control.get_current_box():   #  Progress bar stats
        box = op_control.get_current_box()   #  Progress bar stats
        
        chance = random.random()*0.25 + 0.5
        
        for z in range(box.min_z, box.max_z):
            for x in range(box.min_x, box.max_x):
                y = box.max_y
                keep_going = True
                while y >= box.min_y and keep_going:
                    y -= 1
                    blocks_processed += 1    #  Progress bar stats
                    block_here, block_entity_here = world_context.block_at(x, y, z)
                    #  print(block_here)
                    if block_here != None and block_here in blocks_plantable:
                        block_above, block_entity_above = world_context.block_at(x, y+1, z)
                        if block_above == Block("minecraft", "air", {}):   #  Air
                            print(block_here)
                            if random.random() < chance:
                                world_context.set_block_at(
                                    int(x),
                                    int(y+1),
                                    int(z),
                                    random.choice(world_context.saplings),   #   The populated block type
                                    None,
                                )
                            keep_going = False # Break!
            yield op_control.show_progress_by_blocks_processed(blocks_processed)   #  Progress bar stats
            
        box = op_control.get_next_box()   #  Progress bar stats

export = {"name": "Blanket TWF (v1)", "operation": perform}










