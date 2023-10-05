from CORES.TkinterController import TkinterController
from SCRIPTS.StateController import StateController, States
from SCRIPTS.DATA.GameDataStorage import GameDataStorage, SearchBy
from SCRIPTS.HELPERS.KeyBoardInput import KeyBoardInput
from tkinter import Tk

class MainGUI(Tk):
    def __init__(self, h, w, title, s_w=False, s_h=False, bg='#211717'):
        super().__init__()
        self.TkinterController = TkinterController()
        self.state_controller = StateController()
        self.game_data_storage = GameDataStorage()
        self.ignore_destruction = []
        self.ai_controlled = False
        self.w = w
        self.h = h
        self.bg = bg
        self.set_values(h, w, title, s_w, s_h, bg)

    def set_values(self, h, w, title, s_w=False, s_h=False, bg='#211717'):
        self.title(title)
        self.geometry(f"{w}x{h}")
        self.resizable(width=s_w, height=s_h)
        self.configure(bg=bg)

        self.ignore_destruction.append(
            self.TkinterController.add_checkbox(
                gui=self,
                text="AI Controlled?",
                command=self.toggle_ai_control,
                bg="#D566FF", fg="#000000",
                w=int(w / 11.6), h=1,
                p_x=10, p_y=10
            )
        )

        self.ignore_destruction.append(
            self.TkinterController.add_button(
                gui=self,
                text="Start Next Step",
                command=self.start_next_step,
                bg="#66FFA7", fg="#000000",
                w=int(w / 11.4), h=1,
                p_x=10, p_y=47
            )
        )

        self.update_gui(w)

    def update_gui(self, w):
        for widget in self.winfo_children():
            if not widget in self.ignore_destruction:
                widget.destroy()

        self.TkinterController.add_text(
            gui=self,
            text=self.state_controller.return_state() + "...",
            bg="#949494", fg="#3d3d3d",
            w=int(w / 11.3), h=1,
            p_x=10, p_y=88
        )

    def toggle_ai_control(self, checkbox_var):
        if checkbox_var == 1:
            self.ai_controlled = True
        else:
            self.ai_controlled = False

    def start_next_step(self):
        next_state = self.state_controller.trigger_state_machine()
        self.update_gui(self.w)
        if next_state == States.LOADING:
            print("Loading....")
        elif next_state == States.STARTING_GAME:
            print("Starting....")
        elif next_state == States.GEN_PLAYER_HAND_DATA:
            print("GEN_PLAYER_HAND_DATA....")
            self.game_data_storage.gen_player_hand_data()
        elif next_state == States.GEN_COMBINATIONS_FROM_PLAYER_HAND:
            print("GEN COMBOS....")
            fusions_to_make = self.game_data_storage.gen_player_combinations()
            highest_card = self.game_data_storage.return_best_card_to_summon(fusions_to_make, SearchBy.ATK)
            self.game_data_storage.play_highest_card(highest_card)
        elif next_state == States.END_TURN:
            print("End Turn.....")
            self.game_data_storage.end_turn()