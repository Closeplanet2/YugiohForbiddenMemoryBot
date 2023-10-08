from CORES.JSONController import JSONController
from difflib import SequenceMatcher
from enum import Enum

class SearchMethod(Enum):
    ATK = 1

class CardCore:
    def __init__(self):
        self.stored_cards = JSONController().return_dict_from_json("DATA/CardData.json")
        self.fusion_combos = JSONController().return_dict_from_json("DATA/FusionData.json")

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

    def compare_text_with_description_return_highest(self, text):
        highest_score = 0
        highest_card = None
        for card in self.stored_cards['Cards']:
            score = SequenceMatcher(None, card['CardName'], text).ratio()
            if score > highest_score:
                highest_score = score
                highest_card = card
        return highest_card

    def return_best_option_for_player(self, player_hand, search_method):
        if search_method is SearchMethod.ATK: return self.return_best_option_for_player_ATK(player_hand)

    def return_best_option_for_player_ATK(self, player_hand):
        highest_atk = 0
        highest_card = None
        is_fusion = False

        for card in player_hand:
            if len(card['CardATK']) == 0: continue
            if int(card['CardATK']) > highest_atk:
                highest_atk = int(card['CardATK'])
                highest_card = card
                is_fusion = False

        for card in self.return_all_fusions_based_on_hand(player_hand):
            if len(card['CardATK']) == 0: continue
            if int(card['CardATK']) > highest_atk:
                highest_atk = int(card['CardATK'])
                highest_card = card
                is_fusion = True

        return highest_card, is_fusion

    def return_all_fusions_based_on_hand(self, player_hand):
        fusions_to_make = []
        for fusion_id in self.fusion_combos:
            for player_card in player_hand:
                if player_card['CardID'] in self.fusion_combos[fusion_id]:
                    other_cards_in_combos = self.fusion_combos[fusion_id][player_card['CardID']]
                    for other_player_card in player_hand:
                        if not player_card is other_player_card: continue
                        if other_player_card['CardID'] in other_cards_in_combos:
                            fusions_to_make.append(self.return_card_from_id(fusion_id))
        return fusions_to_make