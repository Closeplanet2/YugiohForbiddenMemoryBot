from SCRIPTS.HELPERS.KeyBoardInput import KeyBoardInput
from SCRIPTS.HELPERS.WindowCapture import WindowCapture
from CORES.JSONController import JSONController
from difflib import SequenceMatcher
from PIL import Image
from enum import Enum
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class SearchBy(Enum):
    ATK = 1

class GameDataStorage:
    def __init__(self):
        self.window_capture = WindowCapture()
        self.player_hand = []
        self.player_monsters = []
        self.stored_cards = JSONController().return_dict_from_json("DATA/CardData.json")
        self.fusion_combos = JSONController().return_dict_from_json("DATA/FusionData.json")

    def gen_player_hand_data(self):
        self.player_hand.clear()
        KeyBoardInput().click_pos(77, 188)
        KeyBoardInput().click_button('x')
        for i in range(0, 5, 1):  KeyBoardInput().left_click_button()
        for i in range(0, 5, 1):
            KeyBoardInput().click_button('s')
            card = self.convert_on_screen_to_card()
            self.player_hand.append(card)
            KeyBoardInput().click_button('x')
            KeyBoardInput().right_click_button()

    def gen_player_combinations(self):
        fusions_to_make = []
        for fusion_id in self.fusion_combos:
            for player_card in self.player_hand:
                if player_card['CardID'] in self.fusion_combos[fusion_id]:
                    other_cards_in_combos = self.fusion_combos[fusion_id][player_card['CardID']]
                    for other_player_card in self.player_hand:
                        if not player_card is other_player_card: continue
                        if other_player_card['CardID'] in other_cards_in_combos:
                            fusions_to_make.append(self.return_card_from_id(fusion_id))
        return fusions_to_make

    def return_best_card_to_summon(self, fusions_to_make, searchBY):
        if searchBY == SearchBy.ATK:
            highest_atk = 0
            highest_card = None
            for card in fusions_to_make:
                if len(card['CardATK']) == 0: continue
                if int(card['CardATK']) > highest_atk:
                    highest_atk = int(card['CardATK'])
                    highest_card = card
            for card in self.player_hand:
                if len(card['CardATK']) == 0: continue
                if int(card['CardATK']) > highest_atk:
                    highest_atk = int(card['CardATK'])
                    highest_card = card
            return highest_card

    def play_highest_card(self, card_to_play):
        KeyBoardInput().click_pos(77, 188)
        print(card_to_play)
        count = 0
        for card_in_hand in self.player_hand:
            if card_in_hand['CardID'] == card_to_play['CardID']:
                for i in range(0, 5, 1):  KeyBoardInput().left_click_button()
                for i in range(0, count, 1): KeyBoardInput().right_click_button()
                KeyBoardInput().click_button('z')
                KeyBoardInput().right_click_button()
                KeyBoardInput().click_button('z')
                for i in range(0, len(self.player_monsters), 1): KeyBoardInput().right_click_button()
                KeyBoardInput().click_button('z')
                KeyBoardInput().click_button('z')
            count += 1

    def end_turn(self):
        KeyBoardInput().enter_click_button()

    def convert_on_screen_to_card(self):
        screenshot = self.window_capture.get_cv_screenshot()
        top_left = (515, 465)
        bottom_right = (808, 920)
        cropped_screenshot = screenshot[top_left[0]:bottom_right[0], top_left[1]:bottom_right[1]]
        text = pytesseract.image_to_string(Image.fromarray(cropped_screenshot), lang="eng")
        return self.compare_text_with_description_return_highest(text)

    def compare_text_with_description_return_highest(self, text):
        highest_score = 0
        highest_card = None
        for card in self.stored_cards['Cards']:
            score = SequenceMatcher(None, card['CardDesc'], text).ratio()
            if score > highest_score:
                highest_score = score
                highest_card = card
        return highest_card

    def return_card_from_id(self, cardID):
        for card in self.stored_cards['Cards']:
            if card['CardID'] == cardID:
                return card
        return None





