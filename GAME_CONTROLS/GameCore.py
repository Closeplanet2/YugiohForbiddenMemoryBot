from CORES.TkinterController import TkinterController, DestructionStage
from CORES.ScreenGrabController import ScreenGrabController
from CORES.InputController import InputController
from CORES.TextController import TextController
from CORES.JSONController import JSONController
from GAME_CONTROLS.CardStorageCore import CardStorageCore, CardAreas
from GAME_CONTROLS.CardImageCore import CardImageCore
from GAME_CONTROLS.StateCore import StateCore, States
from GAME_CONTROLS.CursorCore import CursorCore
from difflib import SequenceMatcher
import time

window_title = "Yu-gi-oh Forbidden Memories"
window_background_color = "#211717"
window_height = 900
window_width = 400

class GameCore:
    def __init__(self, debug_info=False):
        self.debug_info = debug_info
        self.TkinterController = TkinterController(debug_info=self.debug_info)
        self.ScreenGrabController = ScreenGrabController("RetroArch Beetle PSX HW 0.9.44.1 88929ae")
        self.InputController = InputController()
        self.CardStorageCore = CardStorageCore()
        self.CardImageCore = CardImageCore()
        self.TextController = TextController()
        self.StateCore = StateCore()
        self.stored_cards = JSONController().return_dict_from_json("DATA/CardData.json")
        self.CursorCore = CursorCore(0, 4, self.callback_down, self.callback_up)
        self.create_window()

    def create_window(self):
        self.TkinterController.create_window(wh=window_height, ww=window_width, wt=window_title, bg=window_background_color)
        self.TkinterController.add_callback_function(self.create_player_hand_images)
        self.TkinterController.add_callback_function(self.TkinterController.destroy_widgets)
        self.TkinterController.add_label(
            text="Cards In Hand", bg="#64FAFF", fg="#000000", w=int(window_width / 11), h=1, x_pos=0, y_pos=5,
            destroy_status=DestructionStage.DONT_DESTROY
        )
        self.TkinterController.add_label(
            text="Cards On Field", bg="#64FAFF", fg="#000000", w=int(window_width / 11), h=1, x_pos=0, y_pos=175,
            destroy_status=DestructionStage.DONT_DESTROY
        )
        self.TkinterController.add_button(
            text="Next State!", function_callback=self.next_state_button_callback, bg="#FF8181", fg="#000000", w=int(window_width / 11),
            h=1, x_pos=0, y_pos=862, destroy_status=DestructionStage.DONT_DESTROY
        )
        self.TkinterController.start_window()

    def create_player_hand_images(self, gui_window):
        for i in range(0, 5, 1):
            card = self.CardStorageCore.return_card_from_index(CardAreas.Player_Hand, i)
            card_image = self.CardImageCore.return_card_image(card)
            self.TkinterController.add_image_as_grid(
                card_image=card_image, w=70, h=120, pos_x=5, pos_y=40, offset_x=79, offest_y=160, numx=5,
                numy=1, index=i, destroy_status=DestructionStage.DELAYED_DESTROY
            )
        time.sleep(0.5)

    def next_state_button_callback(self):
        next_state = self.StateCore.trigger_state_machine(loop_once=True)
        if next_state is States.GEN_HAND_DATA: self.gen_player_hand_data()

    def callback_down(self, new_cursor_position):
        self.InputController.left_click_button()

    def callback_up(self, new_cursor_position):
        self.InputController.right_click_button()

    def gen_player_hand_data(self):
        if self.debug_info: print("[STARTING HAND GEN]")
        self.CardStorageCore.clean_area(CardAreas.Player_Hand)
        screen_pos = self.ScreenGrabController.convert_pos(pos_x=30, pos_y=30)
        self.InputController.click_pos(posx=screen_pos[0], posy=screen_pos[1])
        self.InputController.click_button('x')
        self.CursorCore.default_cursor()
        for i in range(0, 5, 1):
            self.CursorCore.set_cursor_position(i)
            screenshot = self.ScreenGrabController.take_screenshot()
            screenshot = screenshot.crop((35, 676, 588, 742))
            screenshot_text = self.TextController.image_to_text_pillow(pil_image=screenshot)
            card = self.compare_text_with_description_return_highest(screenshot_text)
            if self.debug_info: print(card)
            self.CardStorageCore.add_card_to_area(CardAreas.Player_Hand, card)

    def compare_text_with_description_return_highest(self, text):
        highest_score = 0
        highest_card = None
        for card in self.stored_cards['Cards']:
            score = SequenceMatcher(None, card['CardName'], text).ratio()
            if score > highest_score:
                highest_score = score
                highest_card = card
        return highest_card
