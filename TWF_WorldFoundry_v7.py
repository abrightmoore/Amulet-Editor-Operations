# This filter is for casting Worlds from the raw potential of code
# abrightmoore@yahoo.com.au
# http://brightmoore.net
# My filters may include code and inspiration from PYMCLEVEL/MCEDIT mentors @Texelelf, @Sethbling, @CodeWarrior0, @Podshot_

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2
from random import *
from numpy import *
from os import listdir
from os.path import isfile, join
import glob
from copy import deepcopy
from random import Random
from PIL import Image

#  @TheWorldFoundry

from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

from amulet.api.block import Block  # For working with Blocks
from amulet.api.block_entity import BlockEntity
from amulet_nbt import *  # For working with block properties

import math
import random
import json

# GLOBAL
CHUNKSIZE = 16

# Filter pseudocode:
#

inputs = (
		("World Foundry", "label"),
		("Divisions:", 30),
		("Radius:",50),
		("Wiggle:",6),
		("Operation:", (
			"Surface",
			"Wireframe",
			"Noise",

  		    )),
		("Palette:", (	"Random",
						"Stone",
						"Earth",
						"Lava",
						"Custom"
					)),
		("Custom Blocks:", ("string","value=95:3 22:0 24:2 19:0 18:0 3:0 1:0 80:0")	),
		("Seed:", 1),
		("Ocean:", False),
		("Core:", False),
		("Clouds:", False),
		("Cloud Material:", Block("minecraft", "white_wool", {})),	
		("Transparency Threshold", 128),
		("Filename:", ("string","value=")),
		("abrightmoore@yahoo.com.au", "label"),
		("http://brightmoore.net", "label"),
)
#  Shim to port MCEdit inputs to options
options1 = {}    #  Shim to port MCEdit inputs to options
for part in inputs: #  Shim to port MCEdit inputs to options
    options1[part[0]] = part[1]  #  Shim to port MCEdit inputs to options
print(options1)
print(options1["Seed:"])

class WorldContext:
    blocks = [
        (Block("minecraft", "air", {}),None),
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


def createSign(level, x, y, z, text): #abrightmoore - convenience method. Due to Jigarbov - this is not a Sign.
    ALIASKEY = "WORLD NUMBER"
    COMMANDBLOCK = 137
    CHUNKSIZE = 16
    STANDING_SIGN = 63
    
    setBlock(level, (STANDING_SIGN,8), x, y, z)
    setBlock(level, (1,0), x, y-1, z)
    control = TAG_Compound()
    control["id"] = TAG_String("Sign")
    control["Text1"] = TAG_String(ALIASKEY)
    control["Text2"] = TAG_String(text)
    control["Text3"] = TAG_String("Generated by")
    control["Text4"] = TAG_String("@abrightmoore")  
    
    control["x"] = TAG_Int(x)
    control["y"] = TAG_Int(y)
    control["z"] = TAG_Int(z)
    chunka = level.getChunk((int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE))
    chunka.TileEntities.append(control)
    chunka.dirty = True

def worldGeometry(RAND, BASERADIUS, DIVISIONS, WIGGLE):
    ANGLEDELTA = 2*pi/(DIVISIONS+1)
    OFFSETANGLELAT = pi/DIVISIONS
    ANGLEDELTALAT = (pi-OFFSETANGLELAT*2)/DIVISIONS
    aWorld = [[BASERADIUS+RAND.randint(-WIGGLE,WIGGLE) for x in range(DIVISIONS)] for x in range(DIVISIONS)]
    
    for i in range(RAND.randint(0,DIVISIONS)):
        x = RAND.randint(0,DIVISIONS-1)
        y = RAND.randint(0,DIVISIONS-1)
        w0 = 0
        if WIGGLE > 0:
            w0 = RAND.randint(1,WIGGLE)
        aWorld[x][y] = aWorld[x][y]-w0

    return aWorld

def worldBuilder(level,box,options):
    method = "worldBuilder"
    (method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)    
    print("Seed:")
    PARAM = int(options["Seed:"])
    if PARAM == 0:
        PARAM = randint(0,99999999999)
    print(PARAM)
    RAND = Random(PARAM)

    # MAXWIGGLE = 8
    
    R = centreWidth
    if centreHeight < R:
        R= centreHeight
    if centreDepth < R:
        R= centreDepth
    
    
    DIVISIONS = options["Divisions:"]
    if DIVISIONS < 3:
        DIVISIONS = RAND.randint(20,60)
    BASERADIUS = options["Radius:"] # R-MAXWIGGLE-RAND.randint(0,int(R/3))
    if BASERADIUS < 1:
        BASERADIUS = R-MAXWIGGLE-RAND.randint(0,int(R/3))
    WIGGLE = options["Wiggle:"]
    if WIGGLE < 1:
        WIGGLE = RAND.randint(2,MAXWIGGLE)

    OPERATION = options["Operation:"]
    
    if OPERATION == "Wireframe":
        materialFill = level.blocks[0] # AIR
    
    # A world is a planet spheroid defined by a bunch of altitudes from the centre
    aWorld = worldGeometry(RAND, BASERADIUS, DIVISIONS, WIGGLE)
    
    # plot the world in the selection box
    cx = (box.min_x + box.max_x) >> 1 # centreWidth
    cy = (box.min_y + box.max_y) >> 1 # centreHeight
    cz = (box.min_z + box.max_z) >> 1 # centreDepth
    
    ANGLEDELTA = 2*pi/(DIVISIONS+1)
    OFFSETANGLELAT = pi/DIVISIONS
    ANGLEDELTALAT = (pi-OFFSETANGLELAT*2)/DIVISIONS
    aWorldWiggle = [[RAND.randint(-1,1)*ANGLEDELTALAT/3 for x in range(DIVISIONS)] for x in range(DIVISIONS)]

    print('Pallette Selection')
#    palette = []
#    palette.append( [ (1,0),(1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (80,0) ] ) # Stone
#    palette.append( [ (95,3),(22,0), (24,2), (19,0), (18,0), (3,0), (1,0), (80,0) ] ) # Earth
#    palette.append( [ (11,0),(11,0), (11,0), (11,0), (11,0), (11,0), (11,0), (11,0) ]   ) # Lava
#    palette.append( [ (49,0),(11,0), (11,0), (11,0), (11,0), (11,0), (11,0), (11,0) ]   ) # Lava with Obsidian base
#    colours = "15 7 8 0 6 2 10 11 3 9 13 5 4 1 14 12".split() # I like this sequence
#    coloursList = map(int, colours)
#    coloursListLen = len(coloursList)
    RAND2 = Random(42)

    blocks = level.blocks
    
    #  print(blocks)
    print('Pallette Selection complete')
    
    print("Forging the planet...")
    
    # do the top and bottom bit
    NorthPole = BASERADIUS+RAND.randint(-WIGGLE,WIGGLE)
    SouthPole = BASERADIUS+RAND.randint(-WIGGLE,WIGGLE)

    RENDERWORLD = True
    if RENDERWORLD == True:
        for longitude in range(0,DIVISIONS+1): # http://www.bbc.co.uk/staticarchive/e344e73982934a546e4c9909087547478672e9ad.png
            if longitude%1 == 0:
                print(longitude)
            
            for latitude in range(0,DIVISIONS):
                
                longAngle1 = ANGLEDELTA * longitude + aWorldWiggle[longitude%DIVISIONS][(latitude)%DIVISIONS]
                latAngle1 = -pi/2+OFFSETANGLELAT+ANGLEDELTALAT * latitude + aWorldWiggle[longitude%DIVISIONS][(latitude)%DIVISIONS]
                longAngle2 = ANGLEDELTA * (longitude+1) + aWorldWiggle[(longitude+1)%DIVISIONS][(latitude)]
                latAngle2 = -pi/2+OFFSETANGLELAT+ANGLEDELTALAT * (latitude+1) + aWorldWiggle[longitude%DIVISIONS][(latitude+1)%DIVISIONS]

                
                (x1,z1,y1) = ((aWorld[(longitude)%DIVISIONS][(latitude)%DIVISIONS] * cos(longAngle1) * cos(latAngle1) ),
                              (aWorld[(longitude)%DIVISIONS][(latitude)%DIVISIONS] * sin(longAngle1) * cos(latAngle1) ),
                              (aWorld[(longitude)%DIVISIONS][(latitude)%DIVISIONS] * sin(latAngle1) ))
                (x2,z2,y2) = ((aWorld[(longitude)%DIVISIONS][(latitude+1)%DIVISIONS] * cos(longAngle1) * cos(latAngle2) ),
                              (aWorld[(longitude)%DIVISIONS][(latitude+1)%DIVISIONS] * sin(longAngle1) * cos(latAngle2) ),
                              (aWorld[(longitude)%DIVISIONS][(latitude+1)%DIVISIONS] * sin(latAngle2) ))
                (x3,z3,y3) = ((aWorld[(longitude+1)%DIVISIONS][(latitude+1)%DIVISIONS] * cos(longAngle2) * cos(latAngle2) ),
                              (aWorld[(longitude+1)%DIVISIONS][(latitude+1)%DIVISIONS] * sin(longAngle2) * cos(latAngle2) ),
                              (aWorld[(longitude+1)%DIVISIONS][(latitude+1)%DIVISIONS] * sin(latAngle2) ))
                (x4,z4,y4) = ((aWorld[(longitude+1)%DIVISIONS][(latitude)%DIVISIONS] * cos(longAngle2) * cos(latAngle1) ),
                              (aWorld[(longitude+1)%DIVISIONS][(latitude)%DIVISIONS] * sin(longAngle2) * cos(latAngle1) ),
                              (aWorld[(longitude+1)%DIVISIONS][(latitude)%DIVISIONS] * sin(latAngle1) ))
                (x0,z0,y0) = ((x1+x2+x3+x4)/4,(z1+z2+z3+z4)/4,(y1+y2+y3+y4)/4)

                if OPERATION == "Wireframe":
                    drawTriangleEdge(level, box, options, (cx+x1,cy+y1,cz+z1),(cx+x2,cy+y2,cz+z2),(cx+x0,cy+y0,cz+z0), blocks[PARAM%len(blocks)])
                    drawTriangleEdge(level, box, options, (cx+x2,cy+y2,cz+z2),(cx+x3,cy+y3,cz+z3),(cx+x0,cy+y0,cz+z0), blocks[PARAM%len(blocks)])
                    drawTriangleEdge(level, box, options, (cx+x3,cy+y3,cz+z3),(cx+x4,cy+y4,cz+z4),(cx+x0,cy+y0,cz+z0), blocks[PARAM%len(blocks)])
                    drawTriangleEdge(level, box, options, (cx+x4,cy+y4,cz+z4),(cx+x1,cy+y1,cz+z1),(cx+x0,cy+y0,cz+z0), blocks[PARAM%len(blocks)])
                    
                else:   
                    drawTriangleColour(level, box, options, (0,0,0), (cx+x1,cy+y1,cz+z1),(cx+x2,cy+y2,cz+z2),(cx+x0,cy+y0,cz+z0), blocks, (cx,cy,cz), BASERADIUS)
                    drawTriangleColour(level, box, options, (0,0,0), (cx+x2,cy+y2,cz+z2),(cx+x3,cy+y3,cz+z3),(cx+x0,cy+y0,cz+z0), blocks, (cx,cy,cz), BASERADIUS)
                    drawTriangleColour(level, box, options, (0,0,0), (cx+x3,cy+y3,cz+z3),(cx+x4,cy+y4,cz+z4),(cx+x0,cy+y0,cz+z0), blocks, (cx,cy,cz), BASERADIUS)
                    drawTriangleColour(level, box, options, (0,0,0), (cx+x4,cy+y4,cz+z4),(cx+x1,cy+y1,cz+z1),(cx+x0,cy+y0,cz+z0), blocks, (cx,cy,cz), BASERADIUS)
                
                    if latitude == 0: # South pole
                        latAngle3 = -pi/2
                        R2 = SouthPole
                        (x5,z5,y5) = ((R2 * cos(longAngle1) * cos(latAngle3) ),
                                  (R2 * sin(longAngle1) * cos(latAngle3) ),
                                  (R2 * sin(latAngle3) ))
                        drawTriangleColour(level, box, options, (0,0,0),(cx+x2,cy+y2,cz+z2),(cx+x3,cy+y3,cz+z3),(cx+x5,cy+y5,cz+z5), blocks, (cx,cy,cz), BASERADIUS)

                    if latitude == DIVISIONS-1:
                        latAngle3 = pi/2
                        R2 = NorthPole
                        (x5,z5,y5) = ((R2 * cos(longAngle2) * cos(latAngle3) ),
                                  (R2 * sin(longAngle2) * cos(latAngle3) ),
                                  (R2 * sin(latAngle3) ))
                        drawTriangleColour(level, box, options, (0,0,0),(cx+x1,cy+y1,cz+z1),(cx+x4,cy+y4,cz+z4),(cx+x5,cy+y5,cz+z5), blocks, (cx,cy,cz), BASERADIUS)
    
    if options["Ocean:"] == True:
        print("Ocean...")
        for y in range(0,height):
            if y%10 == 0:
                print(y)
            for z in range(0,depth):
                for x in range(0,width):
                    dx = x-cx
                    dy = y-cy
                    dz = z-cz
                    dist = sqrt(dx*dx+dy*dy+dz*dz)
                    if dist < BASERADIUS and dist >= BASERADIUS-WIGGLE:
                        block = getBlock(level,x,y,z)
                        if block == blocks[0][0]: # AIR
                            setBlock(level,blocks[1],x,y,z)

    if options["Core:"] == True:
        print("Core...")
        for y in range(0,height):
            if y%10 == 0:
                print(y)
            for z in range(0,depth):
                for x in range(0,width):
                    dx = x-cx
                    dy = y-cy
                    dz = z-cz
                    dist = sqrt(dx*dx+dy*dy+dz*dz)
                    if dist <= BASERADIUS-WIGGLE:
                        block = getBlock(level,x,y,z)
                        if block == blocks[0][0]: # AIR
                            if RAND.randint(0,100) < 10:
                                setBlock(level,blocks[RAND.randint(0,len(blocks)-1)],x,y,z)
                            else:
                                setBlock(level,blocks[int(dist)%len(blocks)],x,y,z)
    '''
    if options["Clouds:"] == True:
        print("Clouds...")
        tempDiv = DIVISIONS
        tempWorld = aWorld
        
        TRANSPARENCY_T = options["Transparency Threshold"]
        CLOUDMATERIALID = options["Cloud Material:"].ID
        filenameTop = options["Filename:"]
        filenameTop = filenameTop.strip()
        if filenameTop == "":
            filenameTop = askOpenFile("Select a Cloud image...", False)
        f = open(filenameTop, "rb")
        data = f.read()
        f.close()
        reader = None # png.Reader(bytes=data) # @Sethbling
        (w, h, pixels1, metadata) = reader.asRGBA8() # @Sethbling
        pixels = list(pixels1) # @Sethbling     

        DIVISIONS = w
        aWorld = worldGeometry(RAND, BASERADIUS+9, DIVISIONS, 0)
        ANGLEDELTA = 2*pi/(DIVISIONS+1)
        OFFSETANGLELAT = pi/DIVISIONS
        ANGLEDELTALAT = (pi-OFFSETANGLELAT*2)/DIVISIONS
        aWorldWiggle = [[RAND.randint(-1,1)*ANGLEDELTALAT/3 for x in range(DIVISIONS)] for x in range(DIVISIONS)]
        cloudLayer = [[(0.1,0.1,0.1) for x in range(DIVISIONS)] for x in range(DIVISIONS)]

        p = 0
        q = 0
        (px,py,pz) = (0,0,0) # Init
        for longitude in range(0,DIVISIONS):
            if longitude%100 == 0:
                print(longitude)
            for latitude in range(0,DIVISIONS):
                longAngle1 = ANGLEDELTA * longitude + aWorldWiggle[longitude%DIVISIONS][(latitude)%DIVISIONS]
                latAngle1 = -pi/2+OFFSETANGLELAT+ANGLEDELTALAT * latitude + aWorldWiggle[longitude%DIVISIONS][(latitude)%DIVISIONS]

                (x1,z1,y1) = ((aWorld[(longitude)%DIVISIONS][(latitude)%DIVISIONS] * cos(longAngle1) * cos(latAngle1) ),
                              (aWorld[(longitude)%DIVISIONS][(latitude)%DIVISIONS] * sin(longAngle1) * cos(latAngle1) ),
                              (aWorld[(longitude)%DIVISIONS][(latitude)%DIVISIONS] * sin(latAngle1) ))
                cloudLayer[longitude][latitude] = (cx+x1,cy+y1,cz+z1)

                colour = getPixel(pixels, (DIVISIONS-longitude)%h, (DIVISIONS-latitude)%w) # after @Sethbling
                if opaque(colour, TRANSPARENCY_T): # @Sethbling
                    (theBlock, theBlockData) = closestMaterial(colour) # @Sethbling
                    (r,g,b,a) = colour
                    (x_,y_,z_) = cloudLayer[int(longitude)%DIVISIONS][int(latitude)%DIVISIONS]
                    setBlock(level, (CLOUDMATERIALID,theBlockData), x_,y_,z_ )
    '''                
                
        # Cloud swirly shapes- \\\insert sekrit text here
#       p = 0
#       q = 0
#       (px,py,pz) = (0,0,0) # Init
#       for i in xrange(0,1000):
#           p = 4*DIVISIONS * sin(i*pi/180)
#           q = 5*DIVISIONS * cos(i*pi/180)
#
#            # (px,py,pz) = cloudLayer[int(p)%DIVISIONS][int(q)%DIVISIONS]
#           if i > 0:
#               c = 0
#               for qx, qy, qz in bresenham.bresenham((int(p),0,int(q)),(int(r),0,int(s))):
#                   if c > 0:
#                       drawLine(level, blocks[len(blocks)-1], cloudLayer[int(qx)%DIVISIONS][int(qz)%DIVISIONS], cloudLayer[int(px1)%DIVISIONS][int(pz1)%DIVISIONS])
#                   (px1,py1,pz1) = (qx,qy,qz)
#                   c = c+1
                    
#           (r,s) = (p,q)   

#       c = 0
#       for qx, qy, qz in bresenham.bresenham((int(DIVISIONS/2),0,int(DIVISIONS/2)),(int(DIVISIONS/2),0,int(0))):
#           if c > 0:
#               drawLine(level, blocks[len(blocks)-4], cloudLayer[int(qx)][int(qz)], cloudLayer[int(px1)][int(pz1)])
#           (px1,py1,pz1) = (qx,qy,qz)
#           c = c+1         
#
#        DIVISIONS = tempDiv
#        aWorld = tempWorld
#
#    createSign(level, cx, cy, cz, str(PARAM))
    
    FuncEnd(level,box,options,method)
    
def getPixel(pixels, x, y): # @Sethbling
    idx = x*4
    return (pixels[y][idx], pixels[y][idx+1], pixels[y][idx+2], pixels[y][idx+3])
    
def transparent(col):
    (r, g, b, a) = col
    return a < 128
    
def opaque(col, threshold):
    (r, g, b, a) = col
    return a >= threshold
    
def closestMaterial(col): # @Sethbling
    (r, g, b, a) = col
    closest = 255*255*3
    best = (35, 0)
    for (mat, dat, mr, mg, mb) in materials:
        (dr, dg, db) = (r-mr, g-mg, b-mb)
        dist = dr*dr+dg*dg+db*db
        if dist < closest:
            closest = dist
            best = (mat, dat)
    return best


def drawTriangleColour(level, box, options, orig, p1, p2, p3, blocks, centre, radius):
    # method = "drawTriangleColour"
    # (method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)    

    (ox, oy, oz) = orig
    (p1x, p1y, p1z) = p1
    (p2x, p2y, p2z) = p2
    (p3x, p3y, p3z) = p3
    
    # for each step along the 'base' draw a line from the apex
    dx = p3x - p2x
    dy = p3y - p2y
    dz = p3z - p2z

    distHoriz = dx*dx + dz*dz
    distance = sqrt(dy*dy + distHoriz)
    
    phi = atan2(dy, sqrt(distHoriz))
    theta = atan2(dz, dx)



    iter = 0
    while iter <= distance:
        (px, py, pz) = ((int)(p2x+iter*cos(theta)*cos(phi)), (int)(p2y+iter*sin(phi)), (int)(p2z+iter*sin(theta)*cos(phi)))
        iter = iter+0.5 # slightly oversample because I lack faith.

        drawLineColour(level, (ox+px, oy+py, oz+pz), (ox+p1x, oy+p1y, oz+p1z), blocks, centre, radius ) 

def drawTriangleEdge(level, box, options, p1, p2, p3, materialEdge):
    # method = "drawTriangleEdge"
    # (method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)    
    (p1x, p1y, p1z) = p1
    (p2x, p2y, p2z) = p2
    (p3x, p3y, p3z) = p3
    drawLine(level, materialEdge, (p1x, p1y, p1z), (p2x, p2y, p2z) )
    drawLine(level, materialEdge, (p1x, p1y, p1z), (p3x, p3y, p3z) )
    drawLine(level, materialEdge, (p2x, p2y, p2z), (p3x, p3y, p3z) )
        

    
    
####################################### CLASSES 
def makeSomeNoise(width, height, depth, R): # Other function names considered were: ShoutOutLoud and BoomBoomShakeTheRoom
    method = "makeSomeNoise"
    # create a noise 
    noise = zeros((width,height,depth))
    for x in range(width):
        for z in range(depth):
            for y in range(height):
                noise[x][y][z] = R.random()
    return noise

def cosineInterpolate(a, b, x): # http://www.minecraftforum.net/forums/off-topic/computer-science-and-technology/482027-generating-perlin-noise?page=4
    ft = pi * x
    f = ((1.0 - cos(ft)) * 0.5)
    ret = a * (1.0 - f) + b * f
    return ret

    
def perlinoise3D(level,box,options,R):
    # Ok this isn't really Perlin. It's my quick kludge
    # method = "perlmanoise3D"
    # (method, (width, height, depth), (centreWidth, centreHeight, centreDepth)) = FuncStart(level,box,options,method)    
    SQRT2 = sqrt(2)
    # Raise the roof (Make some noise)
    noise = makeSomeNoiseRange(width, height, depth, R, -1,1)
    persistence = 2.0
    
    for x in range(0,width):
        if x%10 == 0:
            print(x)
        for z in range(0,depth):
            for y in range(0,height):
                n=0.0
                stepSizeMin = 4.0
                for octave in range(1,2):
                    #v = persistence**octave
                    #v_int = int(v)
                    stepSize = stepSizeMin*persistence*octave
                    px_int = int(x/stepSize)    # Noise sample location
                    pz_int = int(z/stepSize)
                    py_int = int(y/stepSize)
                    pdx_float = x-(px_int*stepSize) # position within the cell
                    pdz_float = z-(pz_int*stepSize)
                    pdy_float = y-(py_int*stepSize)
                    # I need to find what the noise value is within this cell.
                    rdx = pdx_float/stepSize #0.5+cos(pi+pi*dx/v_int)/2
                    rdz = pdz_float/stepSize #0.5+cos(pi+pi*dz/v_int)/2
                    rdy = pdy_float/stepSize #0.5+cos(pi+pi*dz/v_int)/2
                    
                    p000 = noise[px_int][py_int][pz_int]
                    p001 = noise[px_int][py_int][(pz_int+1)%depth]
                    p010 = noise[px_int][(py_int+1)%height][pz_int]
                    p011 = noise[px_int][(py_int+1)%height][(pz_int+1)%depth]                   
                    p100 = noise[(px_int+1)%width][py_int][pz_int]                  
                    p101 = noise[(px_int+1)%width][py_int][(pz_int+1)%depth]                    
                    p110 = noise[(px_int+1)%width][(py_int+1)%height][pz_int]                   
                    p111 = noise[(px_int+1)%width][(py_int+1)%height][(pz_int+1)%depth]                 
            
                    dvx1 = cosineInterpolate(p000,p100,rdx) #
                    dvx2 = cosineInterpolate(p010,p110,rdx)
                    dvx3 = cosineInterpolate(p001,p101,rdx) #
                    dvx4 = cosineInterpolate(p011,p111,rdx)


                    dvz1 = cosineInterpolate(dvx1,dvx3,rdz) #
                    dvz2 = cosineInterpolate(dvx2,dvx4,rdz) #


                    n = n+cosineInterpolate(dvz1,dvz2,rdy)-(sin(pi*y/height))

                    # Draw it
                    if n > 0.8:
                        setBlock(level,(155,0),box.minx+x,box.miny+y,box.minz+z)
                    elif n > 0.6:
                        setBlock(level,(1,0),box.minx+x,box.miny+y,box.minz+z)
                    elif n > 0.5:
                        setBlock(level,(1,1),box.minx+x,box.miny+y,box.minz+z)
                    elif n > 0.0:
                        setBlock(level,(1,2),box.minx+x,box.miny+y,box.minz+z)
                    elif n > -0.2:
                        setBlock(level,(1,3),box.minx+x,box.miny+y,box.minz+z)
                    elif n > -0.3:
                        setBlock(level,(1,4),box.minx+x,box.miny+y,box.minz+z)
                    elif n > -0.4:
                        setBlock(level,(1,5),box.minx+x,box.miny+y,box.minz+z)
                    elif n > -0.8:
                        setBlock(level,(1,6),box.minx+x,box.miny+y,box.minz+z)

        
    FuncEnd(level,box,options,method)

    
####################################### LIBS
    
def FuncStart(level, box, options, method):
    # abrightmoore -> shim to prepare a function.
    print('%s: Started at %s' % (method, time.ctime()))
    (width, height, depth) = (box.max_x - box.min_x, box.max_y - box.min_y, box.max_z - box.min_z)
    centreWidth = math.floor(width / 2)
    centreHeight = math.floor(height / 2)
    centreDepth = math.floor(depth / 2) 
    # other initialisation methods go here
    return (method, (width, height, depth), (centreWidth, centreHeight, centreDepth))

def FuncEnd(level, box, options, method):
    print('%s: Ended at %s' % (method, time.ctime()))
    
def getBoxSize(box):
    return (box.max_x - box.min_x, box.max_y - box.min_y, box.max_z - box.min_z)

def getBlock(level,x,y,z):
    return level.block_at(x,y,z)

def setBlock(level, b, x, y, z):
    # method = "setBlock"
    # print (method, "START")
    
    (block, data) = b
    level.set_block_at(int(x), int(y), int(z), block, data)
    
# Ye Olde GFX Libraries
def drawLine(level, b, p, p1 ):
    # method = "drawLine"
    # print (method, "START")
    

    (blockID, blockData) = b
    (x,y,z) = p
    (x1,y1,z1) = p1
    drawLineConstrained(level, (blockID, blockData), (x,y,z), (x1,y1,z1), 0 )

def drawLineColour(level, p, p1, blocks, centre, radius ):
    # method = "drawLineColour"
    # print (method, "START")

    (x,y,z) = p
    (x1,y1,z1) = p1
    drawLineConstrainedColour(level, (x,y,z), (x1,y1,z1), 0, blocks, centre, radius )

'''
def drawLineBresenham(scratchpad, b, p, p1 ):
    (blockID, blockData) = b
    (x,y,z) = p
    (x1,y1,z1) = p1
    for px, py, pz in bresenham.bresenham((x,y,z),(x1,y1,z1)):
        setBlock(scratchpad,(blockID, blockData),px,py,pz)
    setBlock(scratchpad,(blockID, blockData),x1,y1,z1)
'''
   
   
def drawLineConstrainedColour(level, p, p1, maxLength, blocks, c, BASERADIUS ):
    (x,y,z) = p
    (x1,y1,z1) = p1
    (cx,cy,cz) = c
    
    dx = x1 - x
    dy = y1 - y
    dz = z1 - z

    distHoriz = dx*dx + dz*dz
    distance = sqrt(dy*dy + distHoriz)

    if distance < maxLength or maxLength < 1:
        phi = atan2(dy, sqrt(distHoriz))
        theta = atan2(dz, dx)
        px = 0
        py = 0
        pz = 0
        ddx = 0
        ddy = 0
        ddz = 0
        
        iter = 0
        while iter <= distance:
            ix = (int)(x+iter*cos(theta)*cos(phi))
            iy = (int)(y+iter*sin(phi))
            iz = (int)(z+iter*sin(theta)*cos(phi))

            ddx = ix-cx
            ddy = iy-cy
            ddz = iz-cz

            dist = sqrt(ddx*ddx+ddy*ddy+ddz*ddz)
            if dist < BASERADIUS-1:
                setBlock(level,blocks[0],ix,iy,iz) # Sea
            elif dist < BASERADIUS:
                setBlock(level,blocks[1],ix,iy,iz) # Lapis
            elif dist < BASERADIUS+1:
                setBlock(level,blocks[2],ix,iy,iz) # Sand
            elif dist < BASERADIUS+2:
                setBlock(level,blocks[3],ix,iy,iz) # Plain
            elif dist < BASERADIUS+3:
                setBlock(level,blocks[4],ix,iy,iz) # Forest
            elif dist < BASERADIUS+4:
                setBlock(level,blocks[5],ix,iy,iz) # Mt
            elif dist < BASERADIUS+5:
                setBlock(level,blocks[6],ix,iy,iz) # Snow
            elif dist >= BASERADIUS+5:
                setBlock(level,blocks[7],ix,iy,iz) # Snow
            iter = iter+0.5 # slightly oversample because I lack faith.

def drawLineConstrained(scratchpad, b, p, p1, maxLength ):
    (blockID, blockData) = b
    (x,y,z) = p
    (x1,y1,z1) = p1

    dx = x1 - x
    dy = y1 - y
    dz = z1 - z

    distHoriz = dx*dx + dz*dz
    distance = sqrt(dy*dy + distHoriz)

    if distance < maxLength or maxLength < 1:
        phi = atan2(dy, sqrt(distHoriz))
        theta = atan2(dz, dx)

        iter = 0
        while iter <= distance:
            scratchpad.setBlockAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockID)
            scratchpad.setBlockDataAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockData)
            iter = iter+0.5 # slightly oversample because I lack faith.

            
def drawLineConstrainedRandom(scratchpad, b, p, p1, frequency ):
    (blockID, blockData) = b
    (x,y,z) = p
    (x1,y1,z1) = p1
    
    dx = x1 - x
    dy = y1 - y
    dz = z1 - z

    distHoriz = dx*dx + dz*dz
    distance = sqrt(dy*dy + distHoriz)


    phi = atan2(dy, sqrt(distHoriz))
    theta = atan2(dz, dx)

    iter = 0
    while iter <= distance:
        if randint(0,99) < frequency:
            scratchpad.setBlockAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockID)
            scratchpad.setBlockDataAt((int)(x+iter*cos(theta)*cos(phi)), (int)(y+iter*sin(phi)), (int)(z+iter*sin(theta)*cos(phi)), blockData)
        iter = iter+0.5 # slightly oversample because I lack faith.

def perform_twf(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    # level = WorldContext(world, dimension, None)

    # points = {}
    for box in selection:
        # width = box.max_x - box.min_x
        # height = box.max_y - box.min_y
        # depth = box.max_z - box.min_z

        #  spheroid_twf_v1(world_context, box.min_x, box.min_y, box.min_z, width, height, depth)
        #  ellipsoid_twf_v1(world_context, box.min_x, box.min_y, box.min_z, width, height, depth)
        
        worldBuilder(WorldContext(world, dimension, None), box, options1)

export = {"name": "World Foundry TWF (v7)", "operation": perform_twf}