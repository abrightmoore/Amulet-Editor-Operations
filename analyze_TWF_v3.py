# @TheWorldFoundry

from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

import json


def write_json(filename, json_object):
    with open(filename, "w") as outfile:
        json.dump(json_object, outfile, indent=4, sort_keys=True)


def read_json(filename):
    with open(filename, "r") as infile:
        return json.load(infile)


# for those that are new to python 3 the thing after the colon is the object type that the variable should be
def analyze_TWF(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    # world is the object that contains all the data related to the world
    # dimension in a string used to identify the currently loaded dimension. It can be used to access the right dimension from the world
    # selection is an object describing the selections made by the user. It is possible there may not be any boxes selected
    # options will be explored in further examples
    universal_block_count = 0

    # iter_count = len(list(world.get_chunk_slices(selection, dimension)))
    iter_count = len(list(world.get_chunk_slice_box(dimension, selection)))
    count = 0

    results = {}

    print("Analyze Starting")
    for box in selection:
        for x, y, z in box:
            block = world.get_block(x, y, z, dimension)
            block_str = str(block)

            if block_str in results:
                val = results[block_str]
                val += 1
                results[block_str] = val
            else:
                results[block_str] = 1
        count += 1
        yield count / iter_count

    # Print out the dictionary
    print(results)

    # Print out a csv list
    for k in results.keys():
        print(str(results[k]) + " , " + str(k))

    # Save a result json file
    write_json("analyze_results.json", results)


export = {  # This is what the program will actually look for. It describes how the operation will work
    "name": "Analyze (TWF v3)",  # the name of the plugin
    "operation": analyze_TWF,  # the actual function to call when running the plugin
}
