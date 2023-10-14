from CORES.JSONController import JSONController
from difflib import SequenceMatcher
from enum import Enum

class SearchMethod(Enum):
    ATK = 1

class CardPositions(Enum):
    ATK = 1
    DEF = 2

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

    def return_all_fusion_materials_from_players_hand(self, fusion_monster, player_hand):
        index_a = -1
        index_b = -1
        card_a = None
        card_b = None
        for fusion_a_id in self.fusion_combos[fusion_monster['CardID']]:
            for fusion_b_id in self.fusion_combos[fusion_monster['CardID']][fusion_a_id]:
                if not self.is_card_in_player_hand(player_hand, fusion_a_id): continue
                if not self.is_card_in_player_hand(player_hand, fusion_b_id): continue
                index_a = self.return_card_index(player_hand, fusion_a_id)
                index_b = self.return_card_index(player_hand, fusion_b_id)
                card_a = self.return_card_from_id(fusion_a_id)
                card_b = self.return_card_from_id(fusion_b_id)
                return index_a, index_b, card_a, card_b
        return index_a, index_b, card_a, card_b

    def is_card_in_player_hand(self, player_hand, card_id):
        for card in player_hand:
            if card['CardID'] == card_id: return True
        return False

    def return_card_index(self, player_hand, card_id):
        for i in range(0, len(player_hand), 1):
            if player_hand[i]['CardID'] == card_id: return i
        return None