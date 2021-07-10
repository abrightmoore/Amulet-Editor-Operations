# @TheWorldFoundry

from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension
from amulet_map_editor.programs.edit.api.operations.errors import OperationError

from amulet.api.block import Block  #  For working with Blocks
from amulet.api.block_entity import BlockEntity
from amulet_nbt import *  #  For working with block properties
import random

def get_random_item(world):
    THINGS = ['leather', 'carrot', 'beetroot', 'iron_helmet', 'iron_boots', 'iron_leggings', 'leather_leggings', 'leather_helmet', 'leather_boots', 'clock', 'compass', 'golden_shovel', 'diamond_shovel', 'wooden_shovel', 'stone_shovel', 'iron_shovel', 'flint_and_steel', 'shears', 'golden_chestplate', 'diamond_chestplate', 'chainmail_chestplate', 'iron_chestplate', 'leather_chestplate', 'rotten_flesh', 'bone', 'dye', 'stone', 'grass', 'dirt', 'cobblestone', 'planks', 'sapling', 'sand', 'gravel', 'log', 'leaves', 'glass', 'sandstone', 'deadbush', 'wool', 'yellow_flower', 'red_flower', 'brown_mushroom', 'red_mushroom', 'cactus', 'clay', 'reeds', 'wooden_slab', 'carrots', 'potatoes', 'carpet', 'stick', 'string', 'feather', 'wooden_hoe', 'wheat_seeds', 'leather_boots', 'flint', 'fish', 'cookie', 'pumpkin_seeds', 'melon_seeds', 'rotten_flesh', 'carrot', 'potato', 'poisonous_potato', 'iron_ore', 'coal_ore', 'sponge', 'lapis_ore', 'stone_slab', 'mossy_cobblestone', 'torch', 'oak_stairs', 'redstone_wire', 'wheat', 'ladder', 'stone_stairs', 'wall_sign', 'wooden_pressure_plate', 'stone_button', 'snow', 'fence', 'pumpkin', 'stonebrick', 'melon_block', 'vine', 'waterlily', 'cocoa', 'wooden_button', 'wooden_sword', 'wooden_shovel', 'wooden_pickaxe', 'wooden_axe', 'stone_sword', 'stone_shovel', 'stone_pickaxe', 'stone_axe', 'bowl', 'gunpowder', 'stone_hoe', 'wheat', 'leather_helmet', 'leather_chestplate', 'leather_leggings', 'porkchop', 'sign', 'wooden_door', 'cooked_fished', 'dye', 'bone', 'sugar', 'beef', 'chicken', 'glass_bottle', 'spider_eye', 'experience_bottle', 'writable_book', 'flower_pot', 'baked_potato', 'map', 'name_tag', 'gold_ore', 'lapis_block', 'dispenser', 'golden_rail', 'detector_rail', 'sticky_piston', 'piston', 'brick_block', 'chest', 'diamond_ore', 'furnace', 'rail', 'lever', 'stone_pressure_plate', 'redstone_ore', 'redstone_torch', 'trapdoor', 'iron_bars', 'glass_pane', 'fence_gate', 'brick_stairs', 'stone_brick_stairs', 'sandstone_stairs', 'emerald_ore', 'tripwire_hook', 'tripwire', 'spruce_stairs', 'birch_stairs', 'jungle_stairs', 'cobblestone_wall', 'flower_pot', 'light_weighted_pressure_plate', 'heavy_weighted_pressure_plate', 'redstone_block', 'quartz_ore', 'quartz_block', 'quartz_stairs', 'activator_rail', 'dropper', 'stained_hardened_clay', 'hay_block', 'hardened_clay', 'coal_block', 'packed_ice', 'iron_shovel', 'iron_pickaxe', 'iron_axe', 'flint_and_steel', 'apple', 'bow', 'arrow', 'coal', 'iron_ingot', 'gold_ingot', 'iron_hoe', 'bread', 'cooked_porkchop', 'bucket', 'redstone', 'snowball', 'boat', 'leather', 'milk_bucket', 'brick', 'clay_ball', 'reeds', 'paper', 'book', 'slime_ball', 'chest_minecart', 'furnace_minecart', 'egg', 'compass', 'fishing_rod', 'clock', 'glowstone_dust', 'shears', 'melon', 'cooked_beef', 'cooked_chicken', 'fire_charge', 'pumpkin_pie', 'fireworks', 'firework_charge', 'quartz', 'lead', 'noteblock', 'bed', 'gold_block', 'iron_block', 'tnt', 'bookshelf', 'obsidian', 'diamond_block', 'crafting_table', 'wooden_door', 'iron_door', 'ice', 'jukebox', 'netherrack', 'soul_sand', 'glowstone', 'cake', 'unpowered_repeater', 'brown_mushroom_block', 'red_mushroom_block', 'mycelium', 'nether_brick', 'nether_brick_fence', 'nether_brick_stairs', 'nether_wart', 'enchanting_table', 'brewing_stand', 'cauldron', 'end_stone', 'redstone_lamp', 'ender_chest', 'emerald_block', 'skull', 'anvil', 'trapped_chest', 'powered_comparator', 'daylight_detector', 'hopper', 'diamond', 'iron_sword', 'diamond_sword', 'diamond_shovel', 'diamond_pickaxe', 'diamond_axe', 'mushroom_stew', 'golden_sword', 'golden_shovel', 'golden_pickaxe', 'golden_axe', 'diamond_hoe', 'golden_hoe', 'chainmail_helmet', 'chainmail_chestplate', 'chainmail_leggings', 'chainmail_boots', 'iron_helmet', 'iron_chestplate', 'iron_leggings', 'iron_boots', 'diamond_helmet', 'diamond_chestplate', 'diamond_leggings', 'diamond_boots', 'golden_helmet', 'golden_chestplate', 'golden_leggings', 'golden_boots', 'painting', 'golden_apple', 'water_bucket', 'lava_bucket', 'minecart', 'saddle', 'iron_door', 'cake', 'bed', 'repeater', 'filled_map', 'ender_pearl', 'blaze_rod', 'ghast_tear', 'gold_nugget', 'nether_wart', 'potion', 'fermented_spider_eye', 'blaze_powder', 'magma_cream', 'brewing_stand', 'cauldron', 'ender_eye', 'speckled_melon', 'emerald', 'item_frame', 'golden_carrot', 'skull', 'carrot_on_a_stick', 'nether_star', 'comparator', 'netherbrick', 'tnt_minecart', 'hopper_minecart', 'iron_horse_armor', 'golden_horse_armor', 'diamond_horse_armor', 'record_13', 'record_cat', 'record_blocks', 'record_chirp', 'record_far', 'record_mall', 'record_mellohi', 'record_stal', 'record_strad', 'record_ward', 'record_11', 'record_wait']
    
    prefix = ""
    if world.level_wrapper.platform == "bedrock":
        prefix = "minecraft:"
    
    item = TAG_Compound()
    item["Name"] = TAG_String(prefix+random.choice(THINGS))
    item["Damage"] = TAG_Short(random.randint(0,254))
    item["Count"] = TAG_Byte(1)
    return item


def create_and_fill_a_chest_TWF(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    '''
        This method creates a chest in the selection box with some items within
        @TheWorldFoundry 2021-06-26
    '''
    if world.level_wrapper.platform != "bedrock":
        raise OperationError("This operation only supports Bedrock edition worlds.")
   
    print ("create_and_fill_a_chest Starting")

    block_platform = "bedrock"  # the platform the blocks below are defined in
    block_version = (1, 17, 0)  # the version the blocks below are defined in
    # A chest facing north defined in Bedrock 1.17 format
    block = Block("minecraft", "chest", {"facing_direction": TAG_String("2")})
    
    # Example result:
    # (Block(universal_minecraft:chest[facing="north",type="single"]), 
    # BlockEntity[universal_minecraft:chest, 0, 0, 0]{NBTFile("":{utags: {isMovable: 1b, Findable: 0b, Items: []}})},
    # True)

    for box in selection:  # Set a chest at the lowest x,y,z in each selected box via the user interface
        pos = px, py, pz = box.min_x, box.min_y, box.min_z

        # Make new NBT for this chest with some junk items
        theNBT = TAG_Compound()
        theNBT["isMovable"] = TAG_Byte(1)
        theNBT["Findable"] = TAG_Byte(0)
        theNBT["Items"] = items = TAG_List()
        for i in range(0, random.randint(1, 27)):  #  Collect some junk and pop it in
            item = get_random_item(world)
            item["Slot"] = TAG_Byte(i)
            items.append( item )

        blockEntity = BlockEntity(
            "",
            "Chest",
            0,
            0,
            0,
            NBTFile(
                theNBT
            )
        )
        # Create this chest in the world
        world.set_version_block(px, py, pz, dimension, (block_platform, block_version), block, blockEntity)
        
        # Check what we just created in the world
        block, blockEntity = world.get_version_block(px, py, pz, dimension, (block_platform, block_version))
        print (block)
        print (blockEntity)
        

export = {
    "name": "create_and_fill_a_chest (TWF v1)",
    "operation": create_and_fill_a_chest_TWF
}
