# @TheWorldFoundry

from typing import Tuple, Dict

from amulet.api.selection import SelectionGroup, SelectionBox
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension, BlockCoordinates

from amulet.api.block import Block, UniversalAirBlock  #  For working with Blocks
from amulet.api.block_entity import BlockEntity
from amulet_nbt import *  #  For working with block properties
from math import sin, cos, pi, atan2, sqrt
import random

def enclave(world: BaseLevel, dimension: Dimension, box: SelectionBox):
    '''
        @TheWorldFoundry - take the given selection, work out how big the shape is once rotated around itself
        Map the blocks from the selection to rotated slices pivoting around the lowest-most x,z column.
        
        WARNING: This draws OUTSIDE the selection box (because it has to).
        
        Example animation:
            https://twitter.com/abrightmoore/status/1410897766331523072?s=20
    '''
    twopi = pi * 2.0  #  Precalculate for efficiency
    
    width = box.max_x - box.min_x  # Dimensions of this box
    height = box.max_y - box.min_y
    depth = box.max_z - box.min_z

    # Store the location of each block in the source and the block and block entity in the world's version format
    source_blocks: Dict[BlockCoordinates, Tuple[Block, BlockEntity]] = {}
    for x,y,z in box:
        source_blocks[(x - box.min_x, y - box.min_y, z - box.min_z)] = block_at(world, dimension, x, y, z)
        #  Erase this original block
        world.set_version_block(x, y, z, dimension, ("bedrock", (1, 17, 0)), Block("minecraft", "air"), None)  #  We will be overwriting the space we are sampling. Hint: Work with a pasted copy
    
    #  How many copies will span around the midpoint?
    circumference_mid = twopi * (width >> 1)  #  The inner column gets squeezed and the outer layer gets stretched
    num_copies = circumference_mid / depth  #  Imagine the selection box stacked against itself a number of times
    
    target_blocks = {}
    # For each location in the rotated solid, what is the source block?
    for z in range(box.min_z - width, box.min_z + width + 1):  #  This is the box we will build
        dz = z - box.min_z
        for x in range(box.min_x-width, box.min_x + width + 1):
            #  What is my position in the horizontal plane with respect to the pivot point?
            dx = x - box.min_x
            angle = atan2(dz, dx)
            if angle < 0:
                angle += twopi
            dist_here = sqrt(dx**2 + dz**2)
            dist_circ = angle / twopi * circumference_mid
            px = int(dist_here)
            pz = int(dist_circ)%depth  #  This is the 'remainder'
            for y in range(box.min_y, box.max_y):
                if 0 <= px < width and 0 <= pz < depth:  #  Check bounds
                    if (x, y, z) not in target_blocks:  #  Performance hit - only do a world lookup if we need to
                        block, blockEntity = source_blocks[(px, y - box.min_y, pz)]
                        target_blocks[(x, y, z)] = block, blockEntity

    #  For efficiency sake I'd rather plot the result voxels precisely once
    for x, y, z in target_blocks.keys():
        block, blockEntity = target_blocks[(x, y, z)]
        world.set_version_block(x, y, z, dimension, (world.level_wrapper.platform, world.level_wrapper.version), block, blockEntity)
            
        

def block_at(world, dimension, x, y ,z) -> Tuple[Block, BlockEntity]:
    """Get the block at a given location in the world's version"""
    block, blockEntity = world.get_version_block(x, y ,z, dimension, (world.level_wrapper.platform, world.level_wrapper.version))
    return (block, blockEntity)

def enclave_TWF(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    '''
        Rotate the 3D selection around itself 360 degrees in the horizontal plane.
        
        @TheWorldFoundry 2021-07-01
    '''

    iter_count = len(list(world.get_chunk_slice_box(dimension, selection)))  #  This is for the progress bar that shows when the operation is running
    count = 0  #  This is for the progress bar that shows when the operation is running
    
    print ("surface_TWF Starting")  #  For the console log so I know what button I pressed

    #  This section draws the shape in each selection box with blocks.
    
    for box in selection:
        enclave(world, dimension, box)
        
        count += 1  #  This is for the progress bar that shows when the operation is running
        yield count / iter_count  #  This is for the progress bar that shows when the operation is running

 
export = {
    "name": "enclave_TWF (v1)",
    "operation": enclave_TWF
}
