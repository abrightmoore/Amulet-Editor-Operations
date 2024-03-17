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
from math import pi, cos, sin
from random import randint
import json


#  2024-03-17 KnobblyBox update

OPERATION_NAME = "KNOBBLYBOX TWF 2024 (v1)"

#  This is a static stub to be replaced with the Amulet UI framework
inputs = (
        (OPERATION_NAME, "label"),
        ("Overwrite",True),
        ("adrian@TheWorldFoundry.com", "label"),
        ("http://theworldfoundry.com", "label")
)

#  Shim to port MCEdit inputs to options
options_from_inputs = {}    #  Shim to port MCEdit inputs to options
for part in inputs: #  Shim to port MCEdit inputs to options
    options_from_inputs[part[0]] = part[1]  #  Shim to port MCEdit inputs to options

class WorldContext:
    blocks = [
        (Block("minecraft", "air", {}),None),
        (Block("minecraft", "stone", {}),None),
        (Block("minecraft", "sea_lantern", {}),None),
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

    def set_block(self, x, y, z, block):
        self.set_block_at(x, y, z, block[0], block[1])

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
        print("set_block_at end")

    def get_box_size(self, box):
        return (box.max_x - box.min_x, box.max_y - box.min_y, box.max_z - box.min_z)

def get_points_between_two_points(point1, point2):
    points = []

    # Unpack the coordinates of the two points
    x1, y1 = point1
    x2, y2 = point2

    # Calculate the differences between the coordinates
    dx = x2 - x1
    dy = y2 - y1

    # Determine the number of steps needed based on the maximum difference
    num_steps = max(abs(dx), abs(dy))

    if num_steps == 0:
        # If the two points are the same, return just that point
        return [point1]

    # Calculate the step sizes for x and y
    step_x = dx / num_steps
    step_y = dy / num_steps

    # Generate the points between the two points
    for i in range(int(num_steps) + 1):
        x = x1 + i * step_x
        y = y1 + i * step_y
        points.append((round(x), round(y)))  # Round to integer coordinates

    return points


def knobblybox(world, box, options):
    print(OPERATION_NAME+" started")
    (width, height, depth) = world.get_box_size(box)

    AIR = world.blocks[0]
    material = world.blocks[1]
    insideMaterial = world.blocks[2]
    for x in range(box.min_x,box.max_x):
        for z in range(box.min_z,box.max_z):
            for y in range(box.min_y,box.max_y):
                world.set_block(x, y, z, material)
                

    for x in range(box.min_x+1,box.max_x-1):
        for z in range(box.min_z+1,box.max_z-1):
            for y in range(box.min_y+1,box.max_y-1):
                world.set_block(x, y, z, insideMaterial)
                

    x, y, z = width >> 1, height >> 1, 0
    face = "front"
    d = [0, 1, 0]
    for i in range(int(width+height+depth)>>3,int(width+height+depth)):
        distance = (randint(8,width+depth+height))>>1
        for l in range(distance):
            world.set_block(box.min_x+x, box.min_y+y, box.min_z+z, AIR)
            x += d[0]
            y += d[1]
            z += d[2]
            if d[0] == 1 and x >= width: # We've walked off the right of a face
                if face == "front":
                    d = [0,0,1]
                elif face == "back":
                    d = [0,0,-1]
                elif face == "top":
                    d = [0,-1,0]
                elif face == "bottom":
                    d = [0,1,0]
                face = "right"
                x = width-1
            
            elif d[1] == 1 and y >= height:
                if face == "front":
                    d = [0,0,1]
                elif face == "back":
                    d = [0,0,-1]
                elif face == "right":
                    d = [-1,0,0]
                elif face == "left":
                    d = [1,0,0]
                face = "top"
                y = height-1

            elif d[2] == 1 and z >= depth:
                if face == "right":
                    d = [-1,0,0]
                elif face == "left":
                    d = [1,0,0]
                elif face == "top":
                    d = [0,-1,0]
                elif face == "bottom":
                    d = [0,1,0]
                face = "back"
                z = depth-1

            elif d[0] == -1 and x < 0:
                if face == "front":
                    d = [0,0,1]
                elif face == "back":
                    d = [0,0,-1]
                elif face == "top":
                    d = [0,-1,0]
                elif face == "bottom":
                    d = [0,1,0]
                face = "left"
                x = 0

            elif d[1] == -1 and y < 0:
                if face == "front":
                    d = [0,0,1]
                elif face == "back":
                    d = [0,0,-1]
                elif face == "right":
                    d = [-1,0,0]
                elif face == "left":
                    d = [1,0,0]
                face = "bottom"
                y = 0

            elif d[2] == -1 and z < 0:
                if face == "right":
                    d = [-1,0,0]
                elif face == "left":
                    d = [1,0,0]
                elif face == "top":
                    d = [0,-1,0]
                elif face == "bottom":
                    d = [0,1,0]
                face = "front"
                z = 0
        
        change = randint(1,2)
        if change == 1: # Turn left
            if d == [0, 1, 0] and face == "front":
                d = [-1, 0, 0]
            elif d == [0, 1, 0] and face == "back":
                d = [1, 0, 0]
            elif d == [0, 1, 0] and face == "left":
                d = [0, 0, 1]
            elif d == [0, 1, 0] and face == "right":
                d = [0, 0, -1]
 
            elif d == [0, -1, 0] and face == "front":
                d = [1, 0, 0]
            elif d == [0, -1, 0] and face == "back":
                d = [-1, 0, 0]
            elif d == [0, -1, 0] and face == "left":
                d = [0, 0, -1]
            elif d == [0, -1, 0] and face == "right":
                d = [0, 0, 1]

            elif d == [1, 0, 0] and face == "front":
                d = [0, 1, 0]
            elif d == [1, 0, 0] and face == "back":
                d = [0, -1, 0]
            elif d == [1, 0, 0] and face == "top":
                d = [0, 0, 1]
            elif d == [1, 0, 0] and face == "bottom":
                d = [0, 0, -1]

            elif d == [-1, 0, 0] and face == "front":
                d = [0, -1, 0]
            elif d == [-1, 0, 0] and face == "back":
                d = [0, 1, 0]
            elif d == [-1, 0, 0] and face == "top":
                d = [0, 0, -1]
            elif d == [-1, 0, 0] and face == "bottom":
                d = [0, 0, 1]

            elif d == [0, 0, 1] and face == "right":
                d = [0, 1, 0]
            elif d == [0, 0, 1] and face == "left":
                d = [0, -1, 0]
            elif d == [0, 0, 1] and face == "top":
                d = [-1, 0, 0]
            elif d == [0, 0, 1] and face == "bottom":
                d = [1, 0, 0]

            elif d == [0, 0, -1] and face == "right":
                d = [0, -1, 0]
            elif d == [0, 0, -1] and face == "left":
                d = [0, 1, 0]
            elif d == [0, 0, -1] and face == "top":
                d = [1, 0, 0]
            elif d == [0, 0, -1] and face == "bottom":
                d = [-1, 0, 0]




    print(OPERATION_NAME+" finished")
    


def perform_twf(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    for box in selection:
        knobblybox(WorldContext(world, dimension, None), box, options_from_inputs)

export = {"name": OPERATION_NAME, "operation": perform_twf}    