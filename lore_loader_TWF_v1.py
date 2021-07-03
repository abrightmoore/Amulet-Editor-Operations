# @TheWorldFoundry

from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension

from amulet.api.block import Block  #  For working with Blocks
from amulet.api.block_entity import BlockEntity
from amulet_nbt import *  #  For working with block properties
import random
import json

class Item:
    THINGS = ['leather', 'carrot', 'beetroot', 'iron_helmet', 'iron_boots', 'iron_leggings', 'leather_leggings', 'leather_helmet', 'leather_boots', 'clock', 'compass', 'golden_shovel', 'diamond_shovel', 'wooden_shovel', 'stone_shovel', 'iron_shovel', 'flint_and_steel', 'shears', 'golden_chestplate', 'diamond_chestplate', 'chainmail_chestplate', 'iron_chestplate', 'leather_chestplate', 'rotten_flesh', 'bone', 'dye', 'stone', 'grass', 'dirt', 'cobblestone', 'planks', 'sapling', 'sand', 'gravel', 'log', 'leaves', 'glass', 'sandstone', 'deadbush', 'wool', 'yellow_flower', 'red_flower', 'brown_mushroom', 'red_mushroom', 'cactus', 'clay', 'reeds', 'wooden_slab', 'carrots', 'potatoes', 'carpet', 'stick', 'string', 'feather', 'wooden_hoe', 'wheat_seeds', 'leather_boots', 'flint', 'fish', 'cookie', 'pumpkin_seeds', 'melon_seeds', 'rotten_flesh', 'carrot', 'potato', 'poisonous_potato', 'iron_ore', 'coal_ore', 'sponge', 'lapis_ore', 'stone_slab', 'mossy_cobblestone', 'torch', 'oak_stairs', 'redstone_wire', 'wheat', 'ladder', 'stone_stairs', 'wall_sign', 'wooden_pressure_plate', 'stone_button', 'snow', 'fence', 'pumpkin', 'stonebrick', 'melon_block', 'vine', 'waterlily', 'cocoa', 'wooden_button', 'wooden_sword', 'wooden_shovel', 'wooden_pickaxe', 'wooden_axe', 'stone_sword', 'stone_shovel', 'stone_pickaxe', 'stone_axe', 'bowl', 'gunpowder', 'stone_hoe', 'wheat', 'leather_helmet', 'leather_chestplate', 'leather_leggings', 'porkchop', 'sign', 'wooden_door', 'cooked_fished', 'dye', 'bone', 'sugar', 'beef', 'chicken', 'glass_bottle', 'spider_eye', 'experience_bottle', 'writable_book', 'flower_pot', 'baked_potato', 'map', 'name_tag', 'gold_ore', 'lapis_block', 'dispenser', 'golden_rail', 'detector_rail', 'sticky_piston', 'piston', 'brick_block', 'chest', 'diamond_ore', 'furnace', 'rail', 'lever', 'stone_pressure_plate', 'redstone_ore', 'redstone_torch', 'trapdoor', 'iron_bars', 'glass_pane', 'fence_gate', 'brick_stairs', 'stone_brick_stairs', 'sandstone_stairs', 'emerald_ore', 'tripwire_hook', 'tripwire', 'spruce_stairs', 'birch_stairs', 'jungle_stairs', 'cobblestone_wall', 'flower_pot', 'light_weighted_pressure_plate', 'heavy_weighted_pressure_plate', 'redstone_block', 'quartz_ore', 'quartz_block', 'quartz_stairs', 'activator_rail', 'dropper', 'stained_hardened_clay', 'hay_block', 'hardened_clay', 'coal_block', 'packed_ice', 'iron_shovel', 'iron_pickaxe', 'iron_axe', 'flint_and_steel', 'apple', 'bow', 'arrow', 'coal', 'iron_ingot', 'gold_ingot', 'iron_hoe', 'bread', 'cooked_porkchop', 'bucket', 'redstone', 'snowball', 'boat', 'leather', 'milk_bucket', 'brick', 'clay_ball', 'reeds', 'paper', 'book', 'slime_ball', 'chest_minecart', 'furnace_minecart', 'egg', 'compass', 'fishing_rod', 'clock', 'glowstone_dust', 'shears', 'melon', 'cooked_beef', 'cooked_chicken', 'fire_charge', 'pumpkin_pie', 'fireworks', 'firework_charge', 'quartz', 'lead', 'noteblock', 'bed', 'gold_block', 'iron_block', 'tnt', 'bookshelf', 'obsidian', 'diamond_block', 'crafting_table', 'wooden_door', 'iron_door', 'ice', 'jukebox', 'netherrack', 'soul_sand', 'glowstone', 'cake', 'unpowered_repeater', 'brown_mushroom_block', 'red_mushroom_block', 'mycelium', 'nether_brick', 'nether_brick_fence', 'nether_brick_stairs', 'nether_wart', 'enchanting_table', 'brewing_stand', 'cauldron', 'end_stone', 'redstone_lamp', 'ender_chest', 'emerald_block', 'skull', 'anvil', 'trapped_chest', 'powered_comparator', 'daylight_detector', 'hopper', 'diamond', 'iron_sword', 'diamond_sword', 'diamond_shovel', 'diamond_pickaxe', 'diamond_axe', 'mushroom_stew', 'golden_sword', 'golden_shovel', 'golden_pickaxe', 'golden_axe', 'diamond_hoe', 'golden_hoe', 'chainmail_helmet', 'chainmail_chestplate', 'chainmail_leggings', 'chainmail_boots', 'iron_helmet', 'iron_chestplate', 'iron_leggings', 'iron_boots', 'diamond_helmet', 'diamond_chestplate', 'diamond_leggings', 'diamond_boots', 'golden_helmet', 'golden_chestplate', 'golden_leggings', 'golden_boots', 'painting', 'golden_apple', 'water_bucket', 'lava_bucket', 'minecart', 'saddle', 'iron_door', 'cake', 'bed', 'repeater', 'filled_map', 'ender_pearl', 'blaze_rod', 'ghast_tear', 'gold_nugget', 'nether_wart', 'potion', 'fermented_spider_eye', 'blaze_powder', 'magma_cream', 'brewing_stand', 'cauldron', 'ender_eye', 'speckled_melon', 'emerald', 'item_frame', 'golden_carrot', 'skull', 'carrot_on_a_stick', 'nether_star', 'comparator', 'netherbrick', 'tnt_minecart', 'hopper_minecart', 'iron_horse_armor', 'golden_horse_armor', 'diamond_horse_armor', 'record_13', 'record_cat', 'record_blocks', 'record_chirp', 'record_far', 'record_mall', 'record_mellohi', 'record_stal', 'record_strad', 'record_ward', 'record_11', 'record_wait']

    armor_keys = ["helmet", "boots", "leggings", "chestplate"]
    tools_keys = ["shovel", "pickaxe", "axe", "hoe", "fishing" ]
    melee_keys = ["sword", "axe"]
    ranged_keys = ["bow"]
    all_keys = []
    for a in [ armor_keys, tools_keys, melee_keys, ranged_keys ]:
        for b in a:
            all_keys.append(b)
    
    ENCHANTS =  [ ["Curse of Binding (binding_curse)",1,"Cursed item can not be removed from player",10, armor_keys],
                    ["Curse of Vanishing (vanishing_curse)",1,"Cursed item will disappear after player dies",71, all_keys],
                    ["Depth Strider (depth_strider)",3,"Speeds up how fast you can move underwater",8, armor_keys],
                    ["Efficiency (efficiency)",5,"Increases how fast you can mine",32, tools_keys],
                    ["Feather Falling (feather_falling)",4,"Reduces fall and teleportation damage",2, armor_keys],
                    ["Fire Aspect (fire_aspect)",2,"Sets target on fire",20, melee_keys],
                    ["Fire Protection (fire_protection)",4,"Reduces damage caused by fire and lava",1, armor_keys],
                    ["Flame (flame)",1,"Turns arrows into flaming arrows",50, ranged_keys ],
                    ["Fortune (fortune)",3,"Increases block drops from mining",35, tools_keys],
                    ["Frost Walker (frost_walker)",2,"Freezes water into ice so that you can walk on it (and also allows you to walk on magma blocks without taking damage)",9, armor_keys],
                    ["Infinity (infinity)",1,"Shoots an infinite amount of arrows",51, ranged_keys],
                    ["Knockback (knockback)",2,"Increases knockback dealt (enemies repel backwards)",19, melee_keys],
                    ["Looting (looting)",3,"Increases amount of loot dropped when mob is killed",21, melee_keys],
                    ["Luck of the Sea (luck_of_the_sea)",3,"Increases chances of catching valuable items",61, ["fishing"]],
                    ["Lure (lure)",3,"Increases the rate of fish biting your hook",62, ["fishing"]],
                    ["Mending (mending)",1,"Uses xp to mend your tools, weapons and armor",70, all_keys],
                    ["Power (power)",5,"Increases damage dealt by bow",48, ranged_keys],
                    ["Projectile Protection (projectile_protection)",4,"Reduces projectile damage (arrows, fireballs, fire charges)",4, armor_keys],
                    ["Protection (protection)",4,"General protection against attacks, fire, lava, and falling",0, armor_keys],
                    ["Punch (punch)",2,"Increases knockback dealt (enemies repel backwards)",49, ranged_keys],
                    ["Respiration (respiration)",3,"Extends underwater breathing (see better underwater)",5, armor_keys],
                    ["Sharpness (sharpness)",5,"Increases attack damage dealt to mobs",16, melee_keys],
                    ["Silk Touch (silk_touch)",1,"Mines blocks themselves (fragile items)",33, tools_keys],
                    ["Smite (smite)",3,"Increases attack damage against undead mobs",17, melee_keys],
                    ["Sweeping Edge (sweeping)",3,"Increases damage of sweep attack",22, melee_keys],
                    ["Thorns (thorns)",3,"Causes damage to attackers",7, armor_keys],
                    ["Unbreaking (unbreaking)",3,"Increases durability of item",34, all_keys]
                ]    
    
    BEDROCK_PREFIX = "minecraft:"

    def __init__(self, name):
        self.name = name
        self.display = None
        self.damage = 0
        self.lore = None
        self.enchants = []
    
    def get_random_item_name(self, world):
        prefix = ""
        if world.level_wrapper.platform == "bedrock":
            prefix = "minecraft:"
        return prefix+random.choice(THINGS)

    def set_lore(self, lore):
        #  Maybe do some formatting, line splitting here
        self.lore = lore

    def set_display_name(self, display):
        self.display = display

    def get_NBT(self, count):
        item = TAG_Compound()
        item["Name"] = TAG_String(self.name)
        item["Damage"] = TAG_Short(self.damage)
        item["Count"] = TAG_Byte(count)

        if self.lore is not None or len(self.enchants) > 0 or self.display is not None:
            item["tag"] = TAG_Compound()

        if self.lore is not None or self.display is not None:
            item["tag"]["display"] = TAG_Compound()
            if self.display is not None:
                item["tag"]["display"]["Name"] = TAG_String(self.display)
            if self.lore is not None:
                item["tag"]["display"]["Lore"] = TAG_List()
                for l in self.lore:
                    item["tag"]["display"]["Lore"].append(TAG_String(l))
        

        if len(self.enchants) > 0:
            l = TAG_List()
            for id, lvl in self.enchants:
                m = TAG_Compound()
                m["lvl"] = TAG_Short(lvl)
                m["id"] = TAG_Short(id)
                l.append(m)
            item["tag"]["ench"] = l
        
        return item
        
    def enchant(self, id, lvl):
        self.enchants.append((id, lvl))        

class Container:
    def __init__(self):
        self.contents = {}
        
    def add_item_in_slot(self, slot_num, item, qty):
        self.contents[slot_num] = (item, qty)
    
    def add_item(self, item, qty):
        keys_sorted = sorted(self.contents.keys())
        if len(keys_sorted) == 0:
            self.add_item_in_slot(0, item, qty)
        else:
            for k in keys_sorted:
                if k+1 not in self.contents:
                    self.add_item_in_slot(k+1, item, qty)
                    return
    
    def get_num_slots_chest(self):
        return 28  #  Magic number for a single chest
    
    def get_as_chest_NBT_bedrock(self):
        '''
            This container returned as a Chest NBT object for bedrock.
            Write a different method for other container types.
        '''
        theNBT = TAG_Compound()
        utags = TAG_Compound()
        theNBT["utags"] = utags
        utags["isMovable"] = TAG_Byte(1)
        utags["Findable"] = TAG_Byte(0)
        items = TAG_List()
        
        for i in self.contents.keys():
            #  TODO: Probably should check if the slot is with in the 0-27 range for a chest.
            item, qty = self.contents[i]
            item_NBT = item.get_NBT(qty)
            item_NBT["Slot"] = TAG_Byte(i)
            items.append( item_NBT )
        utags["Items"] = items
        print (theNBT)
        return theNBT

    def create_as_chest_bedrock(self, world, dimension, x, y, z):
        block, blockEntity, isPartial = get_native_block_by_name(world, "minecraft", "chest", {})  # Get a native (not a universal) block to work with
        blockEntity.nbt = self.get_as_chest_NBT_bedrock()
        world.set_version_block(x, y, z, dimension, (world.level_wrapper.platform, world.level_wrapper.version), block, blockEntity)

def get_native_block_by_name(world, namespace, name, properties):
    block, blockEntity, isPartial = world.translation_manager.get_version( world.level_wrapper.platform, world.level_wrapper.version).block.to_universal(Block(namespace, name, properties))
    return (block, blockEntity, isPartial)

def lore_loader_TWF(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):
    '''
        This method creates a chest in the selection box with some items within
        @TheWorldFoundry 2021-06-26
    '''
   
    print ("lore_loader_TWF Starting")

    # Read in the item file
    with open("plugins/operations/lore_loader_input.json", "r") as infile:
        item_json = json.load(infile)
        infile.close()
    
    
    items = []
    for i in item_json:
        item = Item(i["name"])  #  We need at least to know what the item is in Minecraft speak.
        if "damage" in i:
            item.damage = i["damage"]
        if "enchants" in i:
            for e in i["enchants"]:
                item.enchant(e["id"], e["level"])
        if "lore" in i:
            lore = []
            for l in i["lore"]:
                lore.append(l)
                item.set_lore(lore)
        if "display" in i:
            item.set_display_name(i["display"])
        items.append(item)
    
    iteration = 0
    for box in selection:
        # While there are more items to place, keep going
        for x, y, z in box:
            if (x+y+z)%3 == 2 and iteration < len(items):
                slot_count = 0
                chest = Container()
                while iteration < len(items) and slot_count < chest.get_num_slots_chest():  
                    chest.add_item(items[iteration], 1)
                    iteration += 1
                chest.create_as_chest_bedrock(world, dimension, x, y, z)
                # Check what we just created in the world
                block, blockEntity = world.get_version_block(x, y, z, dimension, (world.level_wrapper.platform, world.level_wrapper.version))
                print (block)
                print (blockEntity)
        

export = {
    "name": "lore_loader_TWF (v1)",
    "operation": lore_loader_TWF
}
