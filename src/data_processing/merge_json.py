import glob
import json
import os
import constants
import utils

# find all .json files in that folder
pattern    = os.path.join(constants.REFINED_DIR, "*.json")   
json_paths = glob.glob(pattern)

data_list = []

def merge_jsons(input_folder, output_path):
    """
    Scans input_folder for all .json files, loads them, and merges them into
    one JSON object under top‐level keys equal to each file's basename.
    
    e.g. if you have a.json and b.json:
      merged = { "a": <contents of a.json>,
                 "b": <contents of b.json> }
    """
    merged = {}

    if utils.verify_file(input_folder, replace=False, verbose=True):
        return None
    
    # glob for all json files
    pattern = os.path.join(input_folder, '*.json')
    for filepath in glob.glob(pattern):
        # get basename without extension
        name = os.path.splitext(os.path.basename(filepath))[0]
        
        # load JSON
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # assign under key == filename
        merged[name] = data
    
    # write merged JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)


