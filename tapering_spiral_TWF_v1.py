# @TheWorldFoundry

from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

from amulet.api.block import Block  #  For working with Blocks
from amulet.api.block_entity import BlockEntity
from amulet_nbt import *  #  For working with block properties

import math
import random
import json

def tapering_spiral_TWF(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    block_platform = "bedrock"  # the platform the blocks below are defined in
    block_version = (1, 17, 0)  # the version the blocks below are defined in
    blocks = [
        Block("minecraft", "glowstone", {}),
        Block("minecraft", "wool", { "color": TAG_String("white")}),
        Block("minecraft", "wool", { "color": TAG_String("yellow")}),
        Block("minecraft", "wool", { "color": TAG_String("lime")}),
        Block("minecraft", "wool", { "color": TAG_String("magenta")}),

        
    ]
    
    block_entity = None
    
    for box in selection:
        width = box.max_x - box.min_x
        height = box.max_y - box.min_y
        depth = box.max_z - box.min_z
        
        cx = (box.max_x + box.min_x) >> 1
        cy = (box.max_y + box.min_y) >> 1
        cz = (box.max_z + box.min_z) >> 1
        
        plots = {}
        radius = (width+depth) >> 2

        twopi = math.pi * 2.0
        for i in range(1, 7):
            block = blocks[i%len(blocks)]
            u = 0.0
            
            max_rot = twopi * float(i * 2 + 1)
            ang = twopi/360.0
            while u < max_rot:
                r = u/max_rot * float(radius)
                x = r * math.cos(u)
                y = u/max_rot * float(height)
                z = r * math.sin(u)
                x = cx + int(x)
                y = box.min_y + int(y)
                z = cz + int(z)
                
                world.set_version_block(x, y, z, dimension, (block_platform, block_version), block, block_entity)
               
                u += ang

export = {
    "name": "tapering_spiral_TWF (v1)",
    "operation": tapering_spiral_TWF
}