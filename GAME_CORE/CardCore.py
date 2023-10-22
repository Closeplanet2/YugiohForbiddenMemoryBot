from CORES.JSONController import JSONController
from CORES.WebsiteController import RequestController
from difflib import SequenceMatcher
from PIL import Image
from enum import Enum
import os

class CardType(Enum):
    FUSION_MONSTER = 0
    MONSTER = 1
    SPELL = 2
    TRAP = 3

class PlayStyle(Enum):
    NO_PLAY = 0
    FACE_UP_ATK = 1
    FACE_DOWN_ATK = 2
    FACE_UP_DEF = 3
    FACE_DOWN_DEF = 4

class CardSign(Enum):
    RANDOM = 0
    MERCURY = 1
    NEPTUNE = 2

class CardLocation(Enum):
    HAND = 1
    FIELD = 2

class CardPositions(Enum):
    ATK = 1
    DEF = 2

class CardCore:
    def __init__(self, debug_info=True):
        self.JSONController = JSONController()
        self.stored_cards = self.JSONController.return_dict_from_json("DATA/CardData.json")
        self.fusion_combos = self.JSONController.return_dict_from_json("DATA/FusionData.json")
        self.debug_info = debug_info

    def return_card_from_name(self, card_name):
        for card in self.stored_cards['Cards']:
            if card['CardName'] == card_name:
                return card
        return None

    def return_card_from_id(self, card_id):
        for card in self.stored_cards['Cards']:
            if card['CardID'] == card_id:
                return card
        return None

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

    def return_best_option_for_player(self, player_hand, player_field):
        highest_atk = 0
        highest_card = None
        card_type = CardType.MONSTER
        play_style = PlayStyle.NO_PLAY
        card_sign = CardSign.RANDOM
        index_to_play = len(player_field)

        for card in player_hand:
            if len(card['CardATK']) == 0: continue
            if int(card['CardATK']) > highest_atk:
                highest_atk = int(card['CardATK'])
                highest_card = card
                card_type = CardType.MONSTER
                play_style = PlayStyle.FACE_UP_ATK

        for card in self.return_all_fusions_based_on_cards(player_hand, player_field):
            if len(card['CardATK']) == 0: continue
            if int(card['CardATK']) > highest_atk:
                highest_atk = int(card['CardATK'])
                highest_card = card
                card_type = CardType.FUSION_MONSTER
                play_style = PlayStyle.FACE_UP_ATK

        return highest_card, card_type, play_style, card_sign, index_to_play

    def return_all_fusions_based_on_cards(self, player_hand, player_field):
        fusions_to_make = []
        for fusion_id in self.fusion_combos:
            for index_a in range(0, len(player_hand), 1):
                card_a = player_hand[index_a]
                card_a_id = card_a['CardID']
                if card_a_id in self.fusion_combos[fusion_id]:
                    other_cards_in_combos = self.fusion_combos[fusion_id][card_a_id]
                    for index_b in range(0, len(player_hand), 1):
                        if index_a == index_b: continue
                        card_b = player_hand[index_b]
                        card_b_id = card_b['CardID']
                        if card_b_id in other_cards_in_combos:
                            fusions_to_make.append(self.return_card_from_id(fusion_id))
        return fusions_to_make

    def return_all_fusion_materials_from_players_hand(self, fusion_monster, player_hand, player_field):
        card_a_index = -1
        card_b_index = -1
        card_a_location = CardLocation.HAND
        card_b_location = CardLocation.HAND
        card_a = None
        card_b = None

        for fusion_a_id in self.fusion_combos[fusion_monster['CardID']]:
            for fusion_b_id in self.fusion_combos[fusion_monster['CardID']][fusion_a_id]:
                if not self.is_card_in_area(player_hand, fusion_a_id): continue
                if not self.is_card_in_area(player_hand, fusion_b_id): continue
                card_a = self.return_card_from_id(fusion_a_id)
                card_b = self.return_card_from_id(fusion_b_id)
                card_a_index = self.return_card_index(player_hand, fusion_a_id)
                card_b_index = self.return_card_index(player_hand, fusion_b_id)
                return card_a_index, card_b_index, card_a_location, card_b_location, card_a, card_b

        return card_a_index, card_b_index, card_a_location, card_b_location, card_a, card_b

    def is_card_in_area(self, card_area, card_id):
        for card in card_area:
            if card['CardID'] == card_id: return True
        return False

    def return_card_index(self, card_area, card_id):
        for i in range(0, len(card_area), 1):
            if card_area[i]['CardID'] == card_id: return i
        return None

