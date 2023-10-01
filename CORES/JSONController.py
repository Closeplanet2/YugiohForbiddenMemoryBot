import json
import os

class JSONController:
    def dump_dict_to_json(self, dict, file, overwrite):
        if os.path.exists(file) and overwrite: os.remove(file)
        with open(file, 'w') as fp:
            json.dump(dict, fp)

    def return_dict_from_json(self, file):
        with open(file, "r") as json_file:
            return json.load(json_file)