#  @TheWorldFoundry

#  Amulet Editor standard includes for an operation
from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

from amulet.api.block import Block  # For working with Blocks
from amulet.api.block_entity import BlockEntity
from amulet_nbt import *  # For working with block properties

#  Useful includes for voxel editing
import math
import random
import json

#  2024-01-06 Cylindrificate update

OPERATION_NAME = "CYLINDRIFICATE TWF 2024 (v1)"

#  This is a static stub to be replaced with the Amulet UI framework
inputs = (
		(OPERATION_NAME, "label"),
		("Target Center X:", 0),
		("Target Center Y:", 0),
        ("Target Center Z:", 11500),
        ("Invert:", True),
        #  ("Target Radius:", 500),
		("adrian@theworldfoundry.com", "label"),
		("http://brightmoore.net", "label"),
)
#  Shim to port MCEdit inputs to options
options_from_inputs = {}    #  Shim to port MCEdit inputs to options
for part in inputs: #  Shim to port MCEdit inputs to options
    options_from_inputs[part[0]] = part[1]  #  Shim to port MCEdit inputs to options

class WorldContext:
    blocks = [
        (Block("minecraft", "air", {}),None),
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

    def get_box_size(self, box):
        return (box.max_x - box.min_x, box.max_y - box.min_y, box.max_z - box.min_z)
        
def cylindrificate(world, box, options):
    print(OPERATION_NAME+" started")
    #  Takes the blocks in the selection box and re-maps them to wrap them into a cylinder at the location and of dimensions outlined in the inputs at the top of the script
    (width, height, depth) = world.get_box_size(box)
    
    mu = math.pi * 2.0
    #  print(mu)
    
    #  We're going to iterate through the target space (defined by inputs) and lookup what block should be placed there
    invert = options["Invert:"]
    ox = options["Target Center X:"]
    oy = options["Target Center Y:"]
    oz = options["Target Center Z:"]
    radius = height
    # radius = options["Target Radius:"]
    
    invert_y = 0
    if invert:
        invert_y = height
    
    #   Here we're stepping through the target space voxel positions.
    for x in range(0, width):  #  Target width is the same as source. We're wrapping around this axis.
        tpx = x + ox - (width>>1)    #  Target Position X
        print("Mapping plane "+str(x+1)+" of "+str(width)+" at "+str(tpx))
        for z in range(-radius, radius+1):
            tpz = z + oz    #  Target Position Z
            for y in range(-radius, radius+1):
                tpy = y + oy    #  Target Position Y


                #   The job now is to reach back into the source box to find out what block is defined there.
                #   So I need to find the relative position of the target voxel
                #   The x dimension is easy.
                spx = x + box.min_x  #  1:1 mapping of x planes
                #  How far away from the centre of the cylinder are we? This gives our position up the source box
                dist = math.sqrt(z**2 + y**2)
                spy = float(dist/float(radius)) * float(height)
                if invert:
                    spy = height - spy
                spy = spy + box.min_y
                #  How far around the circle are we? This gives our position in along the depth of the source box
                angle = math.atan2(z, y) + math.pi
                #  print(dist, angle, float(angle / mu))
                spz = (float(angle / mu) * float(depth)) + box.min_z
                # spz = (spz%depth) + box.min_z
                
                #  Now it's a simple copy from source location to target location

                (block, blockentity) = world.block_at(int(spx), int(spy), int(spz))
                #  print("Mapping from "+str((int(spx), int(spy), int(spz)))+" to "+str((int(tpx), int(tpy), int(tpz))))                    
                if dist <= radius and block is not None:
                    #  print("Mapping from "+str((int(spx), int(spy), int(spz)))+" to "+str((int(tpx), int(tpy), int(tpz))))                    
                    world.set_block_at(int(tpx), int(tpy), int(tpz), block, blockentity)
                    #  world.set_block_at(int(spx), int(spy), int(spz), world.blocks[1][0], world.blocks[1][1])  #  Debug
    print(OPERATION_NAME+" finished")
    


def perform_twf(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    # level = WorldContext(world, dimension, None)

    # points = {}
    for box in selection:
        # width = box.max_x - box.min_x
        # height = box.max_y - box.min_y
        # depth = box.max_z - box.min_z

        #  spheroid_twf_v1(world_context, box.min_x, box.min_y, box.min_z, width, height, depth)
        #  ellipsoid_twf_v1(world_context, box.min_x, box.min_y, box.min_z, width, height, depth)
        
        cylindrificate(WorldContext(world, dimension, None), box, options_from_inputs)

export = {"name": OPERATION_NAME, "operation": perform_twf}