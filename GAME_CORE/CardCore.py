from CORES.JSONController import JSONController

class CardCore:
    def __init__(self):
        self.stored_cards = JSONController().return_dict_from_json("DATA/CardData.json")
        self.fusion_combos = JSONController().return_dict_from_json("DATA/FusionData.json")