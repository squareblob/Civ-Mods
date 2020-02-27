# Civ-Mods
A very awful prototype for managing civ related mods and configs. very WIP

## Usage

### Editing

### Add a mod

1. Navigate to [mods.json](https://github.com/squareblob/Civ-Mods/blob/1.14/mods.json)
2. Create a new mod dictionary. 
  1. `"name"` should be lowercase and should begin with alphanumeric character. The name should match the folder in `1.14/configs`
  2. `"type": "resourcepack"` should be included if file added is a resource pack
  3. `"config"` should contain, for each config file in `1.14/configs/<modname>` `<filename>` : `<path in .minecraft folder>`

### Add or edit a config file

1. Navigate to `https://github.com/squareblob/Civ-Mods/tree/1.14/configs`
2. Click on the matching mod folder.
    1. Example : For VoxelMap you would click `https://github.com/squareblob/Civ-Mods/tree/1.14/configs/voxelmap`
    1. If a mod folder does not exist create it, with a name matching the name in mods.json
3. Paste in relevent config files
4. Edit [mods.json](https://github.com/squareblob/Civ-Mods/blob/1.14/mods.json) to include `config`

Alternatively [create an issue](https://github.com/squareblob/Civ-Mods/issues) with attached files. 

