from CORES.JSONController import JSONController

dict = JSONController().return_dict_from_json("DATA/CardData.json")
for card in dict['Cards']:
    card["Position"] = ""
JSONController().dump_dict_to_json(dict, "DATA/CardData.json", True)