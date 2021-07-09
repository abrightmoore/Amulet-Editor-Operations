# @TheWorldFoundry

from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

from amulet.api.block import Block  #  For working with Blocks
from amulet.api.block_entity import BlockEntity
from amulet_nbt import *  #  For working with block properties
from amulet.api.errors import ChunkDoesNotExist, ChunkLoadError

import math
import random
import json

def spawn_sphere_TWF(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    print ("spawn_sphere_TWF starting")
    
    radius = 128
    
    
    rinner = radius-1
    
    r2 = radius**2
    ri2 = rinner**2
    
    block_inside = Block("minecraft", "air", {})  #  This block will be at the centre
    block_edge = Block("minecraft", "stained_glass", {"color" : TAG_String("black")})  #  This block will be the main volume of the sphere
    

    points = {}
    for box in selection:
        
        cx = ((box.max_x + box.min_x) >> 1)
        cy = ((box.max_y + box.min_y) >> 1)
        cz = ((box.max_z + box.min_z) >> 1)
        
        plots = {}

        for y in range(radius+1):
            y2 = y**2
            for z in range(radius+1):
                z2 = z**2
                for x in range(radius+1):
                    x2 = x**2
                    dist = y2 + z2 + x2
                    block = None
                    if dist < r2:
                        block = block_inside
                        if dist >= ri2:
                            block = block_edge
                    if block is not None:
                        points[(cx+x, cy+y, cz+z)] = block
                        points[(cx+x, cy+y, cz-z)] = block
                        points[(cx+x, cy-y, cz+z)] = block
                        points[(cx+x, cy-y, cz-z)] = block
                        points[(cx-x, cy+y, cz+z)] = block
                        points[(cx-x, cy+y, cz-z)] = block
                        points[(cx-x, cy-y, cz+z)] = block
                        points[(cx-x, cy-y, cz-z)] = block

                    
    block_entity = None
    for (x, y, z) in points.keys():
        try:
            block, block_e = world.get_version_block(x, y, z, dimension, (world.level_wrapper.platform, world.level_wrapper.version))

            if "air" in str(block) or "lava" in str(block) or "water" in str(block):
                world.set_version_block(int(x), int(y), int(z), dimension, (world.level_wrapper.platform, world.level_wrapper.version), points[x, y, z], block_entity)
        except ChunkLoadError:
            print ("Unable to load chunk "+str(x>>4)+", "+str(z>>4)+" at coordinates "+str(x)+", "+str(z))
    
    print ("spawn_sphere_TWF ended")
    
            
export = {
    "name": "spawn_sphere_TWF (v1)",
    "operation": spawn_sphere_TWF
}