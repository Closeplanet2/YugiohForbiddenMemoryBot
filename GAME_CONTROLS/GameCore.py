from CORES.TkinterController import TkinterController, DestructionStage
from GAME_CONTROLS.CardStorageCore import CardStorageCore, CardAreas
from GAME_CONTROLS.CardImageCore import CardImageCore
import time

window_title = "Yu-gi-oh Forbidden Memories"
window_background_color = "#211717"
window_height = 900
window_width = 400

class GameCore:
    def __init__(self):
        self.TkinterController = TkinterController(debug_info=False)
        self.CardStorageCore = CardStorageCore()
        self.CardImageCore = CardImageCore()
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
            card = self.CardStorageCore.return_card_from_index(CardAreas.Player_Monsters, i)
            card_image = self.CardImageCore.return_card_image(None if card is None else card['CardName'])
            self.TkinterController.add_image_as_grid(
                card_image=card_image, w=70, h=120, pos_x=5, pos_y=40, offset_x=79, offest_y=160, numx=5,
                numy=1, index=i, destroy_status=DestructionStage.DELAYED_DESTROY
            )

    def next_state_button_callback(self):
        pass