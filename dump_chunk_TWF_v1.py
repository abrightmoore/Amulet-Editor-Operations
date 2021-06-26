# @TheWorldFoundry

from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

# for those that are new to python 3 the thing after the colon is the object type that the variable should be
def dump_chunk_TWF(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    # world is the object that contains all the data related to the world
    # dimension in a string used to identify the currently loaded dimension. It can be used to access the right dimension from the world
    # selection is an object describing the selections made by the user. It is possible there may not be any boxes selected
    # options will be explored in further examples

    iter_count = len(list(world.get_chunk_slice_box(dimension, selection)))
    count = 0
    
    print ("DumpChunk Starting")

    for box in selection.selection_boxes:
        for cx, cz in box.chunk_locations():
            chunk = world.get_chunk(cx, cz, dimension)
            print (chunk)
            
            
        count += 1
        yield count / iter_count
    


export = {  # This is what the program will actually look for. It describes how the operation will work
    "name": "DumpChunk (TWF v1)",  # the name of the plugin
    "operation": dump_chunk_TWF  # the actual function to call when running the plugin
}




