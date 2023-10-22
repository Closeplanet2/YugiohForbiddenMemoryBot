from enum import Enum

class CardAreas(Enum):
    Player_Monsters = 0
    Player_Spells = 1
    Other_Monsters = 2
    Other_Spells = 3
    Player_Hand = 4

class CardStorageCore:
    def __init__(self, debug_info=True):
        self.debug_info = debug_info
        self.callback_functions = []
        self.CardAreas = {}
        self.CardAreas[CardAreas.Player_Monsters.name] = []
        self.CardAreas[CardAreas.Player_Spells.name] = []
        self.CardAreas[CardAreas.Other_Monsters.name] = []
        self.CardAreas[CardAreas.Other_Spells.name] = []
        self.CardAreas[CardAreas.Player_Hand.name] = []

    def add_callback_function(self, callback_function):
        if self.debug_info: print("Added callback function!")
        self.callback_functions.append(callback_function)

    def call_callback_function(self, card_area, card_added, card):
        for callback_function in self.callback_functions:
            callback_function(card_area, card_added, card)

    def return_card_array_from_card_area(self, card_area):
        if card_area is None: return None
        return self.CardAreas[card_area.name]

    def return_card_from_index(self, card_area, index):
        if card_area is None or index is None: return None
        if index >= len(self.CardAreas[card_area.name]): return None
        return self.CardAreas[card_area.name][index]

    def add_card_to_area(self, card_area, card):
        if card_area is None or card is None: return
        if self.debug_info: print(f"Card Added To Area: {card}")
        self.call_callback_function(card_area, True, card)
        self.CardAreas[card_area.name].append(card)

    def remove_card_from_area(self, card_area, card):
        if card_area is None or card is None: return
        if self.debug_info: print(f"Card Removed From Area: {card}")
        self.call_callback_function(card_area, False, card)
        self.CardAreas[card_area.name].remove(card)

    def is_card_in_area(self, card_area, card):
        if card_area is None or card is None: return False
        for x in self.CardAreas[card_area.name]:
            if x['CardID'] == card['CardID']: return True
        return False

    def index_card_from_area(self, card_area, card):
        if card_area is None or card is None: return None
        return self.CardAreas[card_area.name].index(card)

    def clear_card_area(self, card_area, trigger_callback=False):
        if card_area is None: return
        if trigger_callback:
            for card in self.CardAreas[card_area.name]:
                self.call_callback_function(card_area, False, card)
        self.CardAreas[card_area.name].clear()

    def set_card_at_index(self, card_area, index, card):
        if card_area is None or card is None or index is None: return
        self.CardAreas[card_area.name][index] = card

    def pop_card_at_index(self, card_area, index):
        if card_area is None or index is None: return
        card = self.return_card_from_index(card_area, index)
        if card is None: return
        self.call_callback_function(card_area, False, card)
        self.CardAreas[card_area.name].pop(index)

    def return_highest_atk_card_from_area(self, card_area):
        area = self.return_card_array_from_card_area(card_area)
        if area is None: return None
        highest_atk = -1
        highest_card = None
        for card in area:
            card_atk = int(card['CardATK']) if len(card['CardATK']) > 0 else -1
            if card_atk > highest_atk:
                highest_atk = card_atk
                highest_card = card
        return highest_card