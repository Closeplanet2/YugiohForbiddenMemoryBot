from enum import Enum

class CardAreas(Enum):
    Player_Monsters = 0
    Player_Spells = 1
    Other_Monsters = 2
    Other_Spells = 3
    Player_Hand = 4

class CardStorageCore:
    def __init__(self):
        self.CardAreas = {}
        self.CardAreas[CardAreas.Player_Monsters.name] = []
        self.CardAreas[CardAreas.Player_Spells.name] = []
        self.CardAreas[CardAreas.Other_Monsters.name] = []
        self.CardAreas[CardAreas.Other_Spells.name] = []
        self.CardAreas[CardAreas.Player_Hand.name] = []

    def add_card_to_area(self, card_area, card):
        self.CardAreas[card_area.name].append(card)

    def set_card_at_index(self, card_area, index, card):
        self.CardAreas[card_area.name][index] = card

    def return_index_of_object(self, card_area, card):
        return self.CardAreas[card_area.name].index(card)

    def clean_area(self, card_area):
        self.CardAreas[card_area.name].clear()

    def remove_card_from_area(self, card_area, card):
        self.CardAreas[card_area.name].remove(card)

    def pop_card_from_area(self, card_area, card_index):
        self.CardAreas[card_area.name].pop(card_index)

    def return_card_area(self, card_area):
        return self.CardAreas[card_area.name]

    def return_card_from_index(self, card_area, card_index):
        if card_index >= len(self.CardAreas[card_area.name]): return None
        elif card_index < 0: return None
        return self.CardAreas[card_area.name][card_index]

    def return_highest_atk_card_from_area(self, card_area):
        area = self.return_card_area(card_area)
        if area is None: return None
        highest_atk = -1
        highest_card = None
        for card in area:
            card_atk = int(card['CardATK']) if len(card['CardATK']) > 0 else -1
            if card_atk > highest_atk:
                highest_atk = card_atk
                highest_card = card
        return highest_card

    def is_card_in_area_id(self, card_area, card_id):
        for card in self.return_card_area(card_area):
            if card['CardID'] == card_id: return True
        return False


