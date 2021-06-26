# Amulet-Editor-Operations
Authored and Contributed Amulet Editor Operations

* **analyze_TWF_v3.py** (compatible with v0.8.8+) will count the block types in the selection and print the results to the Amulet Editor console, and write the data in JSON format to the file analyze_results.json in your Amulet directory. This Operation is a good example of how to work with the _selection_ to find the co-ordinates of all the selected blocks. It also shows how to work with block metadata in the Amulet Editor Universal format.

* **dump_chunk_TWF_v1.py** (compatible with v0.8.8+) shows how to access the chunks that are intersecting the selection boxes, iterate through them, and write out some of their nbt structures to the Amulet Editor console.

* **set_blocks_from_palette_TWF_v1.py** (compatible with v0.8.8+) fills the selection with random blocks defined in a 'palette' of block types set up within the script. It uses the platform and version information from the loaded level to avoid the user having to specify a particular game version in the script. It also has examples of passing block properties, which need to be set as NBT tags. (I've tried to simplify the block access as much as possible for the user, at the expense of performance).

_More Resources_

**StealthyExpert** is writing and sharing Amulet Editor Operations here: https://github.com/StealthyExpertX/Amulet-Plugins

The Amulet Editor and MCEdit Unified Discord is where all the cool kids hang out. Check the #amulet-plugins channel. Join via https://www.amuletmc.com/, the /r/MCEdit reddit, or with this invite: https://discord.gg/pGUwZb9m65

I'm doing a bit of tweet-devlog over here. Follow for new discoveries, methods and real time discussions: https://twitter.com/abrightmoore/status/1408697813542658048
