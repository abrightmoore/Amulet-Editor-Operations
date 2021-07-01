# @TheWorldFoundry

from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

from amulet.api.block import Block  #  For working with Blocks
from amulet.api.block_entity import BlockEntity
from amulet_nbt import *  #  For working with block properties
from math import sin, cos, pi
import random

def get_native_block_by_name(world, namespace, name, properties):
    block, blockEntity, isPartial = world.translation_manager.get_version( world.level_wrapper.platform, world.level_wrapper.version).block.to_universal(Block(namespace, name, properties))
    return (block, blockEntity, isPartial)

def klein_loop_kangaroo_physics_TWF(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    '''
        Draw a shaped path in the selection boxes.
        
        @TheWorldFoundry 2021-07-01
        
        From https://twitter.com/KangarooPhysics/status/1410303260704055298?s=20
    '''
    
    my_blocks = [
        "minecraft:glowstone"
    ]
    
    iterations = 360*8
    iter_width = 16
    iter_count = len(list(world.get_chunk_slice_box(dimension, selection)))*iterations  #  This is for the progress bar that shows when the operation is running
    count = 0  #  This is for the progress bar that shows when the operation is running
    
    print ("klein_loop_kangaroo_physics_TWF Starting")

    block_names = []
    for my_block in my_blocks:
        namespace, bn = my_block.split(":")
        block_names.append((namespace, bn))

    #  This section draws the shape in each selection box with blocks.
    
    for box in selection:
        
        width = box.max_x - box.min_x  # Dimensions of this box
        height = box.max_y - box.min_y
        depth = box.max_z - box.min_z
        
        radius_width = 1.0 #width >>3
        radius_height = 1.0 #height >>3
        radius_depth = 1.0 #depth >>3
        
        ox = (box.max_x + box.min_x)>>1  # Centrepoint of this box
        oy = (box.max_y + box.min_y)>>1
        oz = (box.max_z + box.min_z)>>1
        
        angle = pi/float(iterations/2)
        
        plot_points = {}
        
        min_x = None
        max_x = None
        min_z = None
        max_z = None
        min_y = None
        max_y = None
        
        for j in range(0, iter_width):
            u = -pi
            v = -pi
            
            for i in range(0, iterations):  #  Number of discrete steps in this process
                a = (1.0 - sin(2*u) * sin(v))
                x = cos(u) * cos(v)/a
                z = sin(u) * cos(v)/a
                y = cos(2.0*u) * sin(v)/a

                x = x * float(radius_width)
                y = y * float(radius_height)
                z = z * float(radius_depth)


                plot_points[(x, y, z)] = True  #  I need this to work out how 'big' the plot it so it can be scaled appropriately
                if min_x == None or x < min_x:
                    min_x = x
                if max_x == None or x > max_x:
                    max_x = x
                if min_z == None or z < min_z:
                    min_z = z
                if max_z == None or z > max_z:
                    max_z = z
                if min_y == None or y < min_y:
                    min_y = y
                if max_y == None or y > max_y:
                    max_y = y
                        
                u += angle
                v += angle


                count += 1  #  This is for the progress bar that shows when the operation is running
                yield count / iter_count  #  This is for the progress bar that shows when the operation is running
                

            radius_width += 0.05  #  This makes a wide path of blocks by drawing it scaled up 
            radius_height += 0.05
            radius_depth += 0.05

            scale_x = (max_x - min_x)  #  This is for rendering into space
            scale_z = (max_z - min_z)
            scale_y = (max_y - min_y)
            
            for x, y, z in plot_points.keys():
                px = (x-min_x)/scale_x * width  #  Normalise to 0, re-scale to box dimensions
                py = (y-min_y)/scale_y * height  #  Normalise to 0, re-scale to box dimensions
                pz = (z-min_z)/scale_z * depth  #  Normalise to 0, re-scale to box dimensions
            
                x = int(px + box.min_x)  # offset from the box lower corner
                y = int(py + box.min_y)
                z = int(pz + box.min_z)

                if box.min_x <= x < box.max_x and box.min_y <= y < box.max_y and box.min_z <= z < box.max_z:  #  Only plot when within box bounds
                    namespace, block_name = random.choice(block_names)  #  Possibly a different block each step if there's more than one in the palette list
                    block, blockEntity, isPartial = get_native_block_by_name(world, namespace, block_name, {})  #  Find a block type of this name in this world
                    world.set_version_block(int(x), int(y), int(z), dimension, (world.level_wrapper.platform, world.level_wrapper.version), block, blockEntity)  #  Write this block into the world at the specified coordinates and dimension


 
export = {
    "name": "klein_loop_kangaroo_physics_TWF (v1)",
    "operation": klein_loop_kangaroo_physics_TWF
}
