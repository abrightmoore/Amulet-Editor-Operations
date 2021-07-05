# @TheWorldFoundry

from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

from amulet.api.block import Block  #  For working with Blocks
from amulet.api.block_entity import BlockEntity
from amulet_nbt import *  #  For working with block properties

def get_version_block_TWF(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    for box in selection:
        for x, y, z in box:
            block, block_entity = world.get_version_block(x, y, z, dimension, (world.level_wrapper.platform, world.level_wrapper.version))
            print (block, block_entity)
            
            

export = {
    "name": "get_version_block_TWF (v1)",
    "operation": get_version_block_TWF
}