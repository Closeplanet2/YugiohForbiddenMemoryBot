from CORES.JSONController import JSONController
from CORES.WebsiteController import RequestController
from difflib import SequenceMatcher
from PIL import Image
import os

class CardCore:
    def __init__(self, debug_info=True):
        self.JSONController = JSONController()
        self.stored_cards = self.JSONController.return_dict_from_json("DATA/CardData.json")
        self.fusion_combos = self.JSONController.return_dict_from_json("DATA/FusionData.json")
        self.debug_info = debug_info

    def return_card_image(self, our_card):
        if our_card is None: return Image.open("IMAGES/CardBack.png")
        if os.path.exists(f"IMAGES/{our_card['CardName']}.png"):
            return Image.open(f"IMAGES/{our_card['CardName']}.png")
        for card in self.stored_cards:
            if our_card['CardName'] == card['name']:
                RequestController().download_image(
                    image_url=card['card_images'][0]['image_url'],
                    save_path=f"IMAGES/{our_card['CardName']}.png"
                )
                if self.debug_info: print(f"Downloaded card image {our_card['CardName']}")
                return Image.open(f"IMAGES/{our_card['CardName']}.png")
        return Image.open("IMAGES/CardBack.png")

    def find_card_with_closest_name(self, text):
        highest_score = 0
        highest_card = None
        for card in self.stored_cards['Cards']:
            score = SequenceMatcher(None, card['CardName'], text).ratio()
            if score > highest_score:
                highest_score = score
                highest_card = card
        return highest_card