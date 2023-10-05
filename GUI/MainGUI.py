from CORES.TkinterController import TkinterController
from CORES.GameDataController import GameDataController
from CORES.StateController import StateController
from tkinter import Tk

class MainGUI(Tk):
    window_height = 900
    window_width = 400
    window_title = "Yu-gi-oh Forbidden Memories"
    scale_width = False
    scale_height = False
    window_background_color = "#211717"

    def __init__(self):
        super().__init__()
        self.TkinterController = TkinterController()
        self.GameDataController = GameDataController()
        self.StateController = StateController()
        self.set_values(
            self.window_height, self.window_width, self.window_title,
            self.scale_width, self.scale_height, self.window_background_color
        )

    def set_values(self, window_height, window_width, window_title, scale_width, scale_height, window_background_color):
        self.title(window_title)
        self.geometry(f"{window_width}x{window_height}")
        self.resizable(width=scale_width, height=scale_height)
        self.configure(bg=window_background_color)
        self.TkinterController.add_ignore_destruction(self.return_cards_in_player_hand_text(window_width))
        self.TkinterController.add_ignore_destruction(self.return_cards_in_player_field_text(window_width))
        self.TkinterController.add_ignore_destruction(self.return_start_game_button(window_width))
        self.update_gui()

    def update_gui(self):
        self.TkinterController.destroy_all_widgets(self)
        hand_images = self.GameDataController.return_array_photos(self.GameDataController.player_hand)
        field_images = self.GameDataController.return_array_photos(self.GameDataController.player_field)
        for i in range(0, 5, 1):
            self.TkinterController.add_image_as_grid(
                gui=self, card_image=hand_images[i], w=70, h=120, pos_x=5, pos_y=40,
                offset_x=79, offest_y=160, numx=5, numy=1, index=i
            )
            self.TkinterController.add_image_as_grid(
                gui=self, card_image=field_images[i], w=70, h=120, pos_x=5, pos_y=210,
                offset_x=79, offest_y=160, numx=5, numy=1, index=i
            )


    def return_cards_in_player_hand_text(self, window_width):
        return self.TkinterController.add_text(
            gui=self, text="Cards In Hand", bg="#64FAFF", fg="#000000",
            w=int(window_width / 11), h=1, p_x=0, p_y=5
        )

    def return_cards_in_player_field_text(self, window_width):
        return self.TkinterController.add_text(
            gui=self, text="Cards On Field", bg="#64FAFF", fg="#000000",
            w=int(window_width / 11), h=1, p_x=0, p_y=175
        )

    def return_start_game_button(self, window_width):
        return self.TkinterController.add_button(
            gui=self, text="Start Game", command=self.trigger_state_machine,
            bg="#A8FF64", fg="#000000", w=int(window_width / 11), h=1,
            p_x=0, p_y=862
        )

    def trigger_state_machine(self):
