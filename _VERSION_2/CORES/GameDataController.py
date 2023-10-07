from CORES.JSONController import JSONController
from CORES.WebsiteController import RequestController
from CORES.SccrenGrabController import SccrenGrabController
from CORES.InputController import InputController
from CORES.TextController import TextController
from PIL import Image
from difflib import SequenceMatcher
import os
import time

class GameDataController:
    def __init__(self):
        self.player_hand = []
        self.player_field = []
        self.other_field = []
        self.cursor_position = 0
        self.turn_count = 0
        self.JSONController = JSONController()
        self.InputController = InputController()
        self.TextController = TextController()
        self.SccrenGrabController = SccrenGrabController("RetroArch Beetle PSX HW 0.9.44.1 88929ae")
        self.stored_cards = JSONController().return_dict_from_json("DATA/CardData.json")
        self.default_cursor_position()

    def click_screen(self):
        mouse_pos = self.SccrenGrabController.convert_pos(30, 30)
        self.InputController.click_pos(mouse_pos[0], mouse_pos[1])

    def default_cursor_position(self):
        self.click_screen()
        self.InputController.click_button('x')
        for i in range(0, 5, 1): self.InputController.left_click_button()
        self.cursor_position = 0

    def set_cursor_position(self, new_position):
        if new_position is self.cursor_position:
            return
        self.click_screen()
        new_position = max(0, min(4, new_position))
        if new_position > self.cursor_position:
            for i in range(self.cursor_position, new_position, 1): self.InputController.right_click_button()
        else:
            for i in range(self.cursor_position, new_position, -1): self.InputController.left_click_button()
        self.cursor_position = new_position

    def gen_hand_data(self, callback_function):
        self.player_hand.clear()
        self.click_screen()
        self.InputController.click_button('x')
        self.set_cursor_position(new_position=0)
        for i in range(0, 5, 1):
            self.set_cursor_position(new_position=i)
            time.sleep(0.5)
            card = self.convert_on_screen_to_card()
            print(card)
            self.player_hand.append(card)
        callback_function()

    def convert_on_screen_to_card(self):
        screenshot = self.SccrenGrabController.take_screenshot()
        cropped_screenshot = screenshot.crop((35, 676, 588, 742))
        text = self.TextController.image_to_text_pillow(pil_image=cropped_screenshot, custom_config=None, save_image=False)
        return self.compare_text_with_description_return_highest(text)

    def compare_text_with_description_return_highest(self, text):
        highest_score = 0
        highest_card = None
        for card in self.stored_cards['Cards']:
            score = SequenceMatcher(None, card['CardName'], text).ratio()
            if score > highest_score:
                highest_score = score
                highest_card = card
        return highest_card

    def return_array_photos(self, array):
        images = []
        for i in range(0, 5, 1):
            data = array[i]['CardName'] if i < len(array) else None
            images.append(self.return_card_photo_url(data))
        return images

    def return_json_data(self):
        return self.JSONController.return_page_as_json("https://db.ygoprodeck.com/api/v7/cardinfo.php")['data']

    def return_card_photo_url(self, card_name):
        if card_name is None:
            return Image.open("IMAGES/CARDS/CardBack.png")
        if os.path.exists(f"IMAGES/CARDS/{card_name}.png"):
            return Image.open(f"IMAGES/CARDS/{card_name}.png")
        for card in self.return_json_data():
            if card_name == card['name']:
                RequestController().download_image(
                    image_url=card['card_images'][0]['image_url'],
                    save_path=f"IMAGES/CARDS/{card_name}.png"
                )
                return Image.open(f"IMAGES/CARDS/{card_name}.png")
        return Image.open("IMAGES/CARDS/CardBack.png")

    def play_card_from_hand(self, highest_card, is_fusion, fusion_material, callback_function):
        self.click_screen()
        index = self.player_hand.index(highest_card)
        self.set_cursor_position(new_position=index)
        self.cursor_position = 0
        self.InputController.click_button('z')
        self.InputController.right_click_button()
        self.InputController.click_button('z')
        self.InputController.click_button('z')
        self.InputController.click_button('z')
        self.InputController.click_button('z')
        self.player_hand.remove(highest_card)
        self.player_field.append(highest_card)
        callback_function()

    def gather_board_info(self, callback_function):
        self.click_screen()
        self.InputController.up_click_button()
        screenshot = self.SccrenGrabController.take_screenshot()
        self.set_cursor_position(new_position=0)
        for i in range(0, 5, 1):
            self.set_cursor_position(new_position=i)
            cropped_screenshot = screenshot.crop((35, 676, 588, 742))
            contains_name = self.SccrenGrabController.does_image_contain_color_pixel(cropped_screenshot, (255, 255, 255))
            if contains_name:
                #TODO Add card to enemy board
                pass
        callback_function()

    def override_player_hand(self, callback_function):
        for card in self.player_hand:
            if input(f"Override card {card['CardName']}? (Y/N) ").lower() == "y":
                new_card = self.return_card_from_name(input("New Card: "))
                if new_card is None: continue
                index = self.player_hand.index(card)
                self.player_hand[index] = new_card
                callback_function()

    def end_turn(self, callback_function):
        self.click_screen()
        self.InputController.enter_click_button()
        callback_function()

    def return_card_from_name(self, card_name):
        for card in self.stored_cards['Cards']:
            if card['CardName'] == card_name:
                return card
        return None
