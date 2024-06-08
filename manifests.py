import argparse
import os
import datetime
import json
import hashlib
from typing import List, Dict

def get_file_hash(file_path) -> str:
    with open(file_path, 'rb') as f:
        content = f.read()
        return hashlib.sha256(content).hexdigest()


def load_patchdata(patachdata_dir) -> Dict:
    gamemodes = [f for f in os.listdir(patachdata_dir) if not f.startswith('.')]
    print ('found gamemodes:', gamemodes)

    patchdata_files = {}

    for gamemode in gamemodes:
        gamemode_manifest = {
            'created_at': datetime.datetime.now(datetime.UTC).isoformat(),
            'gamemode': gamemode,
        }

        gamemode_files = {}

        gamemode_dir = os.path.join(patachdata_dir, gamemode)
        characters_dir = os.path.join(gamemode_dir, 'characters')
        items_dir = os.path.join(gamemode_dir, 'items')

        characters = [f for f in os.listdir(characters_dir) if not f.startswith('.')]
        items = [f for f in os.listdir(items_dir) if not f.startswith('.')]

        for character in characters:
            character_path = os.path.join(characters_dir, character)

            hash = get_file_hash(character_path)
            gamemode_files["characters/" + character] = hash
            patchdata_files[character_path] = hash

        for item in items:
            item_path = os.path.join(items_dir, item)

            hash = get_file_hash(item_path)
            gamemode_files["items/" + item] = hash
            patchdata_files[item_path] = hash

        gamemode_manifest['files'] = gamemode_files

        gamemode_manifest_path = os.path.join(gamemode_dir, 'manifest.json')
        with open(gamemode_manifest_path, 'w') as f:
            f.write(json.dumps(gamemode_manifest, indent=4))

        patchdata_files[gamemode_manifest_path] = get_file_hash(gamemode_manifest_path)
    
    return patchdata_files

def load_asset_type(asset_type_dir) -> Dict:
    files_dict = {}
    files = [f for f in os.listdir(asset_type_dir) if not f.startswith('.')]
    
    for file in files:
        if os.path.isdir(file):
            files_dict.update(load_asset_type(file))
        else:
            file_path = os.path.join(asset_type_dir, file)
            hash = get_file_hash(file_path)
            files_dict[file_path] = hash

    return files_dict

def get_visible_subdir_names(file_path: str) -> str:
    return [f for f in os.listdir(file_path) if os.path.isdir(os.path.join(file_path, f)) and not f.startswith('.')]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--version',
        type=str,
        default='main',
        help='The version that will be written to the manifest files'
    )

    parser.add_argument(
        '--update_url',
        type=str,
        default='https://github.com/OpenChamp/default_assets/releases',
        help='The URL where the client can fetch new versions of the assets'
    )
    
    args = vars(parser.parse_args())

    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_dir)

    # list all folders in the current directory
    asset_groups = get_visible_subdir_names(script_dir)
    print ('found asset groups:', asset_groups)

    main_manifest = {
        'version': args['version'],
        'update_url': args['update_url'],
        'created_at': datetime.datetime.now(datetime.UTC).isoformat(),
        'asset_groups': asset_groups,
    }

    file_data = {}
    
    print('main manifest without hashes:', json.dumps(main_manifest, indent=4))

    for asset_group in asset_groups:
        asset_types =  get_visible_subdir_names(asset_group)

        print ('scanning asset group "', asset_group, '" absolute path:', os.path.abspath(asset_group))
        print ('found asset types "', asset_types, '" in asset group "', asset_group, '"')

        for asset_type in asset_types:
            asset_type_dir = os.path.join(asset_group, asset_type)

            if asset_type == 'patchdata':
                file_data.update(load_patchdata(asset_type_dir))
            else:
                file_data.update(load_asset_type(asset_type_dir))

    main_manifest['files'] = file_data
    with open('manifest.json', 'w') as f:
        f.write(json.dumps(main_manifest, indent=4))
