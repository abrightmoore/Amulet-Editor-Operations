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

def sphere_TWF(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    blocks = [
        Block("minecraft", "air", {}),
        Block("minecraft", "glowstone", {}),
        Block("minecraft", "wool", { "color": TAG_String("white")}),
        Block("minecraft", "wool", { "color": TAG_String("yellow")}),
        Block("minecraft", "wool", { "color": TAG_String("lime")}),
        Block("minecraft", "wool", { "color": TAG_String("magenta")}),
        Block("minecraft", "wool", { "color": TAG_String("pink")}),
        Block("minecraft", "wool", { "color": TAG_String("red")}),
        Block("minecraft", "wool", { "color": TAG_String("black")}),
        Block("minecraft", "wool", { "color": TAG_String("green")}),
        Block("minecraft", "wool", { "color": TAG_String("purple")}),
        Block("minecraft", "wool", { "color": TAG_String("brown")}),
        Block("minecraft", "wool", { "color": TAG_String("silver")}),
        Block("minecraft", "wool", { "color": TAG_String("gray")}),
        
    ]
    
    block1 = random.choice(blocks)
    block2 = random.choice(blocks)
    block3 = random.choice(blocks)
    
    block_entity = None
    points = {}
    for box in selection:
        width = box.max_x - box.min_x
        height = box.max_y - box.min_y
        depth = box.max_z - box.min_z

        x_is_odd = 0 # width%2
        y_is_odd = 0 # height%2
        z_is_odd = 0 # depth%2
        
        cx = ((box.max_x + box.min_x) >> 1)
        cy = ((box.max_y + box.min_y) >> 1)
        cz = ((box.max_z + box.min_z) >> 1)
        
        plots = {}

        a = width>>1
        b = height>>1
        c = depth>>1
        for (x,y,z) in box:
            x = cx-x
            y = cy-y
            z = cz-z

            value = float((x*x)/(a*a) + (y*y)/(b*b) + (z*z)/(c*c))

            if value == 0:
                points[(x+cx-x_is_odd, y+cy-y_is_odd, z+cz-z_is_odd)] = block1
            elif abs(value - 1) < 0.01:
                points[(x+cx-x_is_odd, y+cy-y_is_odd, z+cz-z_is_odd)] = block2
            elif value < 1:
                points[(x+cx-x_is_odd, y+cy-y_is_odd, z+cz-z_is_odd)] = block3
    
    for (x, y, z) in points.keys():
        # print (x,y,z)
        world.set_version_block(int(x), int(y), int(z), dimension, (world.level_wrapper.platform, world.level_wrapper.version), points[x, y, z], block_entity)

export = {
    "name": "sphere_TWF (v1)",
    "operation": sphere_TWF
}