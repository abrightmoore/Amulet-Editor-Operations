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
def bedrock_geometry_export_v2(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    filename = "bedrock_model_"


    # iter_count = len(list(world.get_chunk_slices(selection, dimension)))
    iter_count = len(list(world.get_chunk_slice_box(dimension, selection)))
    count = 0

    results = {}

    print("Bedrock geometry export Starting")
    
    for box in selection:
        cubes = {}
        cx = (box.max_x-box.min_x)/2
        cz = (box.max_z-box.min_z)/2

        for y in range(box.min_y, box.max_y):
            for z in range(box.min_z, box.max_z):
                for x in range(box.min_x, box.max_x):
                    block_str = str(world.get_block(x, y, z, dimension))
                    if "air" not in block_str or "stair" in block_str:
                        cubes[(-(x-box.min_x-cx), (y-box.min_y), (z-box.min_z-cz))] = [1, 1, 1]

        # Collapse adjacent cubes into bigger prisms
        attempts = 10
        keepGoing = True
        while keepGoing == True and attempts > 0:
            attempts -= 1
            keepGoing = False  #  Assume we should break
            result = {}
            deleted = {}
            for (x, y, z) in cubes:
                sh = cubes[(x,y,z)]  # Shape of THIS cube
                if ((x+sh[0], y, z) in cubes) and ((x+sh[0], y, z) not in deleted) and (cubes[(x+sh[0], y, z)][1] == sh[1] and cubes[(x+sh[0], y, z)][2] == sh[2]):
                    
                    result[(x,y,z)] = [sh[0]+cubes[(x+sh[0], y, z)][0], sh[1], sh[2]]
                    cubes[(x+sh[0], y, z)] = [0,0,0]  # No shape for a merged cube
                    deleted[(x, y, z)] = [0,0,0]
                    deleted[(x+sh[0], y, z)] = [0,0,0]  # Safety in case we run across the merged shape
                    keepGoing = True
                    
                elif ((x, y+sh[1], z) in cubes) and ((x, y+sh[1], z) not in deleted) and (cubes[(x, y+sh[1], z)][0] == sh[0] and cubes[(x, y+sh[1], z)][2] == sh[2] ):
                    
                    result[(x,y,z)] = [sh[0], sh[1]+cubes[(x, y+sh[1], z)][1], sh[2]]
                    cubes[(x, y+sh[1], z)] = [0,0,0]  # No shape for a merged cube
                    deleted[(x, y, z)] = [0,0,0]
                    deleted[(x, y+sh[1], z)] = [0,0,0]  # Safety in case we run across the merged shape
                    keepGoing = True
                    
                elif ((x, y, z+sh[2]) in cubes) and ((x, y, z+sh[2]) not in deleted) and (cubes[(x, y, z+sh[2])][0] == sh[0] and cubes[(x, y, z+sh[2])][1] == sh[1]):

                    result[(x,y,z)] = [sh[0], sh[1], sh[2]+cubes[(x, y, z+sh[2])][2]]
                    cubes[(x, y, z+sh[2])] = [0,0,0]  # No shape for a merged cube
                    deleted[(x, y, z)] = [0,0,0]
                    deleted[(x, y, z+sh[2])] = [0,0,0]  # Safety in case we run across the merged shape
                    keepGoing = True
                    
                else:  # No merge - add this cube in
                    result[(x,y,z)] = sh
                    deleted[(x, y, z)] = [0,0,0]
                    
                #  print deleted
            cubes = result


        shapes = []
        i = 0
        for (x,y,z) in cubes:
            i += 1
            sh = cubes[(x,y,z)]
            if sh[0] > 0 and sh[1] > 0 and sh[2] > 0:
                shapes.append({"name": "mceu_cube_"+str(i), "origin": [x, y, z], "size": [sh[0], sh[1], sh[2]], "uv": [0, 0]})
        
        json_object = {
            "format_version": "1.12.0",
            "minecraft:geometry": [
                {
                    "description": {
                        "identifier": "geometry.model",
                        "texture_width": 16,
                        "texture_height": 16,
                        "visible_bounds_width": cx,
                        "visible_bounds_height": box.max_y-box.min_y,
                        "visible_bounds_offset": [0, 0.25, 0]
                    },
                    "bones": [
                        {
                            "name": "bb_main",
                            "pivot": [0, 0, 0],
                            "cubes": shapes
                        }
                    ]
                }
            ]
        }
        
        with open(filename+str(count)+".geo.json", "w") as outfile:
            json.dump(json_object, outfile, indent=4, sort_keys=True)

        count += 1
        yield count / iter_count


export = {  # This is what the program will actually look for. It describes how the operation will work
    "name": "bedrock_geometry_export (TWF v2)",  # the name of the plugin
    "operation": bedrock_geometry_export_v2,  # the actual function to call when running the plugin
}
