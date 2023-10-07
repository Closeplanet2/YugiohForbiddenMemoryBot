from enum import Enum

class CardAreas(Enum):
    Player_Monsters = 0
    Player_Spells = 1
    Other_Monsters = 2
    Other_Spells = 3

class CardStorageCore:
    def __init__(self):
        self.CardAreas = {}
        self.CardAreas[CardAreas.Player_Monsters] = []
        self.CardAreas[CardAreas.Player_Spells] = []
        self.CardAreas[CardAreas.Other_Monsters] = []
        self.CardAreas[CardAreas.Other_Spells] = []

    def add_card_to_area(self, card_area, card):
        self.CardAreas[card_area] = card

    def remove_card_from_area(self, card_area, card):
        self.CardAreas[card_area].remove(card)

    def pop_card_from_area(self, card_area, card_index):
        self.CardAreas[card_area].pop(card_index)

    def return_card_area(self, card_area):
        return self.CardAreas[card_area]

    def return_card_from_index(self, card_area, card_index):
        if card_index >= len(self.CardAreas[card_area]): return None
        elif card_index < 0: return None
        return self.CardAreas[card_area][card_index]