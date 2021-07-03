# Amulet-Editor-Operations
Authored and Contributed Amulet Editor Operations. Based on information from GentleGiantJGC.

* **enclave** * Wrap the selection around a cylinder centred on its lowest x,z point

* **analyze_TWF_v3.py** (compatible with v0.8.8+) will count the block types in the selection and print the results to the Amulet Editor console, and write the data in JSON format to the file analyze_results.json in your Amulet directory. This Operation is a good example of how to work with the _selection_ to find the co-ordinates of all the selected blocks. It also shows how to work with block metadata in the Amulet Editor Universal format.

* **dump_chunk_TWF_v1.py** (compatible with v0.8.8+) shows how to access the chunks that are intersecting the selection boxes, iterate through them, and write out some of their nbt structures to the Amulet Editor console.

* **set_blocks_from_palette_TWF_v1.py** (compatible with v0.8.8+) fills the selection with random blocks defined in a 'palette' of block types set up within the script. It uses the platform and version information from the loaded level to avoid the user having to specify a particular game version in the script. It also has examples of passing block properties, which need to be set as NBT tags. (I've tried to simplify the block access as much as possible for the user, at the expense of performance).

* **clone_to_sky_TWF_v1.py** replicates the selection vertically. Use this to create towers from a single 'floor'. Shows how to access the copy/paste similar to how we would use MCSchematics in the earlier program MCEdit Unified. Includes a helper method to mark the chunks intersecting the selection boxes as dirty.

* **create_and_fill_a_chest_TWF_v1.py** shows how to work with NBT data structures, and block entities in a chunk. This Operation creates a single chest at the lowest selection point and puts some items in it.

* **make_chunk_outline_TWF_v1.py** draws wool in the sky at y-255 around the chunk border.

* **klein_loop_kangaroo_physics_TWF_v1** Some methods for plotting into a selection box in worldspace with a scaled pointcloud.




_More Resources_

**StealthyExpert** is writing and sharing Amulet Editor Operations here: https://github.com/StealthyExpertX/Amulet-Plugins

Amulet Core API docs: https://amulet-core.readthedocs.io/en/stable/api_reference/

The Amulet Editor and MCEdit Unified Discord is where all the cool kids hang out. Check the #amulet-plugins channel. Join via https://www.amuletmc.com/, the /r/MCEdit reddit, or with this invite: https://discord.gg/pGUwZb9m65

I'm doing a bit of tweet-devlog over here. Follow for new discoveries, methods and real time discussions: https://twitter.com/abrightmoore/status/1408697813542658048
