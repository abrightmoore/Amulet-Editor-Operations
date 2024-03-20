#   @TheWorldFoundry


#   Parse a Bedrock Resource Pack
#   Read the definitions for block textures
#   Create a new minimal java block definition resource pack for use in Amulet
#   This should allow the user to see their ingame custom blocks
#   Assumes everything is a cube, relies on the minecraft cube definition

import os
import glob
import shutil
import json
import pygame

block_library = {}
texture_library = {}


respack_path = 'twf_calm_rp'
output_path = 'amulet_rp'
assets = "assets"

os.makedirs(output_path, exist_ok=True)
packmcmeta = {
              "pack": {
                "pack_format": 18,
                "description": "Amulet Custom Blocks Resource Pack"
              }
            }
with open(os.path.join(output_path,"pack.mcmeta"), 'w') as file:
    json.dump(packmcmeta, file, indent=4)

shutil.copy(os.path.join(respack_path,"pack_icon.png"), output_path)

with open(os.path.join(respack_path,"blocks.json"), 'r') as file:
    blocks = json.load(file)

with open(os.path.join(os.path.join(respack_path,"textures"),"terrain_texture.json"), 'r') as file:
    atlas = json.load(file)

for tex in atlas["texture_data"]:
    if type(atlas["texture_data"][tex]["textures"]) is list:
        #   Take the first one
        # print(atlas["texture_data"][tex]["textures"][0])
        if type(atlas["texture_data"][tex]["textures"][0]["variations"][0]) is dict:
            texture_library[tex] = pygame.image.load(os.path.join(respack_path,atlas["texture_data"][tex]["textures"][0]["variations"][0]["path"])+".png")
        else:
            texture_library[tex] = pygame.image.load(os.path.join(respack_path,atlas["texture_data"][tex]["textures"][0]["variations"][0])+".png")
    else:
        texture_library[tex] = pygame.image.load(os.path.join(respack_path,atlas["texture_data"][tex]["textures"])+".png")

for block_id in blocks:
    if block_id != "format_version":
        tex = blocks[block_id]["textures"]
        if type(tex) is dict:
            val = None
            for key in tex:
                val = tex[key]
            tex = val
        
        block_library[block_id] = texture_library[tex]   # my:block = a bitmap
        
        id_parts = block_id.split(":")
        
        namespace = id_parts[0]
        name = id_parts[1]
        
        os.makedirs(os.path.join(os.path.join(os.path.join(output_path,assets),namespace),"blockstates"), exist_ok=True)
        os.makedirs(os.path.join(os.path.join(os.path.join(output_path,assets),namespace),os.path.join("models","block")), exist_ok=True)
        os.makedirs(os.path.join(os.path.join(os.path.join(output_path,assets),namespace),os.path.join("textures","block")), exist_ok=True)
        
        #  Save the texture under the block name in the right namespaced folder
        pygame.image.save(texture_library[tex], os.path.join(os.path.join(os.path.join(os.path.join(output_path,assets),namespace),os.path.join("textures","block")),name+".png"))
        
        blockstates = {
                          "variants": {
                            "": {
                              "model": namespace+":block/"+name
                            }
                          }
                        }
        
        with open(os.path.join(os.path.join(os.path.join(os.path.join(output_path,assets),namespace),"blockstates"),name+".json"), 'w') as file:
            json.dump(blockstates, file, indent=4)
            
        models = {
                      "parent": "minecraft:block/cube_all",
                      "textures": {
                        "all": namespace+":block/"+name
                      }
                    }

        with open(os.path.join(os.path.join(os.path.join(os.path.join(output_path,assets),namespace),os.path.join("models","block")),name+".json"), 'w') as file:
            json.dump(models, file, indent=4)
