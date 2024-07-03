# OpenChamp default assets

This repository contains all the runtime loaded asstes for OpenChamp.

At the moment only lang, textures and patchdata get loaded.
More data types will be available in the game later.

To keep everything as compatible as possible files should not be removed.
If a file needs a change then it gets replaced by another one with the same name.
Since these are the base assets all of the servers and clients will depend on it and we don't want to cause references into nothing by an update.

**All files in here must be lowercase only to prevent problems on some platforms.**

## Structure

All data files go in the openchamp dir and its subdirs.
The base structure is the following:

```
openchamp/
   audio/...
   characters/...
   fonts/...
   lang/...
   maps/...
   materials/...
   models/...
   patchdata/...
   shaders/...
   styles/...
   textures/...
```

### audio

The audio dir contains all audio files.
It has the following structure:

```
audio/
    music/...
    sfx/...
    voice/<char_id>/<locale>/...
```

The audio files require a low of subdirs to properly handle the vast amount of needed data.
Each character will need several voice lines for all the languages, so putting them all in one dir will make it too messy.

### lang

The lang dir contains the translation files.
These can either be optimized translations produced by godot or json files.
The file needs the locale they contains as file basename.

#### lang json format

The json lang files simply contain a top level object.
It is just a collection of key value pairs.

```json
{
    "translation_key_1": "translated text",
    "translation_key_2": "more translations"
}
```

### patchdata

patchdata contains json files for the item and character data specification.
Each file in here should be a json file according to the item file specification.

Note: The filecontent of these files don't get loaded automatically.
However on launch the file content will be put in the patchadat cache.
This may reduce the network traffic the servers have to deal with drastically.

Note2: The manifest files are not part of the repository.
Use the following command to generate all the manifest json files:
```
python manifests.py
```

### textures

The textures should comply to the following structure:

```
textures/
    item/...
    ui/...
    characters/<char_id>/...
```

Again every character gets their own subdir to keep everything organized.
The item textures get their own dir since these will get the most additions/changes.
