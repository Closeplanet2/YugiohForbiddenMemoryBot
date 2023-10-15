from CORES.TkinterController import TkinterController, DestructionStage
from CORES.ScreenGrabController import ScreenGrabController
from CORES.InputController import InputController
from CORES.TextController import TextController
from GAME_CONTROLS.CardStorageCore import CardStorageCore, CardAreas
from GAME_CONTROLS.CardImageCore import CardImageCore
from GAME_CONTROLS.StateCore import StateCore, States
from GAME_CONTROLS.CursorCore import CursorCore
from GAME_CONTROLS.CardCore import CardCore, SearchMethod, CardPositions
import time

window_title = "Yu-gi-oh Forbidden Memories!"
window_background_color = "#211717"
window_height = 900
window_width = 400

#TODO fuse from field as well
#TODO what happens if field is full
#TODO what to do with spell cards
#TODO star sign

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
        self.CardCore = CardCore()
        self.CursorCore = CursorCore(0, 4, self.InputController.left_click_button, self.InputController.right_click_button)
        self.lock_input = False
        self.player_turn_count = -1
        self.create_window()

    def create_window(self):
        self.TkinterController.create_window(wh=window_height, ww=window_width, wt=window_title, bg=window_background_color)
        self.TkinterController.add_callback_function(self.create_player_hand_images)
        self.TkinterController.add_callback_function(self.create_player_field_images)
        self.TkinterController.add_callback_function(self.create_enemy_field_images)
        self.TkinterController.add_callback_function(self.TkinterController.destroy_widgets)
        self.TkinterController.add_label(
            text="Cards In Hand!", bg="#64FAFF", fg="#000000", w=int(window_width / 11), h=1, x_pos=0, y_pos=5,
            destroy_status=DestructionStage.DONT_DESTROY
        )
        self.TkinterController.add_label(
            text="Cards On Field!", bg="#64FAFF", fg="#000000", w=int(window_width / 11), h=1, x_pos=0, y_pos=175,
            destroy_status=DestructionStage.DONT_DESTROY
        )
        self.TkinterController.add_label(
            text="Cards On Enemy Field!", bg="#64FAFF", fg="#000000", w=int(window_width / 11), h=1, x_pos=0, y_pos=475,
            destroy_status=DestructionStage.DONT_DESTROY
        )
        self.TkinterController.add_button(
            text="Next State!", function_callback=self.next_state_button_callback, bg="#FF8181", fg="#000000",
            w=int(window_width / 11),
            h=1, x_pos=0, y_pos=862, destroy_status=DestructionStage.DONT_DESTROY
        )
        self.TkinterController.add_button(
            text="Override Data!", function_callback=self.override_player_data_callback, bg="#FF8181", fg="#000000", w=int(window_width / 11),
            h=1, x_pos=0, y_pos=820, destroy_status=DestructionStage.DONT_DESTROY
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

    def create_player_field_images(self, gui_window):
        for i in range(0, 5, 1):
            monster_card = self.CardStorageCore.return_card_from_index(CardAreas.Player_Monsters, i)
            monster_card_image = self.CardImageCore.return_card_image(monster_card)
            self.TkinterController.add_image_as_grid(
                card_image=monster_card_image, w=70, h=120, pos_x=5, pos_y=210, offset_x=79, offest_y=160, numx=5,
                numy=1, index=i, destroy_status=DestructionStage.DELAYED_DESTROY
            )
            spell_card = self.CardStorageCore.return_card_from_index(CardAreas.Player_Spells, i)
            spell_card_image = self.CardImageCore.return_card_image(spell_card)
            self.TkinterController.add_image_as_grid(
                card_image=spell_card_image, w=70, h=120, pos_x=5, pos_y=340, offset_x=79, offest_y=160, numx=5,
                numy=1, index=i, destroy_status=DestructionStage.DELAYED_DESTROY
            )

    def create_enemy_field_images(self, gui_window):
        for i in range(0, 5, 1):
            monster_card = self.CardStorageCore.return_card_from_index(CardAreas.Other_Monsters, i)
            monster_card_image = self.CardImageCore.return_card_image(monster_card)
            self.TkinterController.add_image_as_grid(
                card_image=monster_card_image, w=70, h=120, pos_x=5, pos_y=510, offset_x=79, offest_y=160, numx=5,
                numy=1, index=i, destroy_status=DestructionStage.DELAYED_DESTROY
            )
            spell_card = self.CardStorageCore.return_card_from_index(CardAreas.Other_Spells, i)
            spell_card_image = self.CardImageCore.return_card_image(spell_card)
            self.TkinterController.add_image_as_grid(
                card_image=spell_card_image, w=70, h=120, pos_x=5, pos_y=639, offset_x=79, offest_y=160, numx=5,
                numy=1, index=i, destroy_status=DestructionStage.DELAYED_DESTROY
            )

    def next_state_button_callback(self):
        if self.lock_input: return
        self.lock_input = True
        next_state = self.StateCore.trigger_state_machine(loop_once=False, ignore_gather_info=self.player_turn_count <= 0, ignore_combat=self.player_turn_count <= 0)
        if next_state is States.GEN_HAND_DATA: self.gen_player_hand_data()
        elif next_state is States.GEN_BEST_CARD_TO_PLAY: self.gen_best_card_to_play_for_player()
        elif next_state is States.GATHER_BOARD_INFO: self.gather_board_info_for_ai()
        elif next_state is States.ATK_PLAYERS_MONSTERS: self.atk_player_monsters()
        elif next_state is States.END_TURN: self.end_turn()
        elif next_state is States.END_PROGRAM: self.end_program()
        else: self.end_program()
        self.lock_input = False

    def override_player_data_callback(self):
        if self.lock_input: return
        self.lock_input = True
        if input("Change Player Hand? (Y/N) ") == "y":
            if len(self.CardStorageCore.return_card_area(CardAreas.Player_Hand)) == 0:
                print("No Hand Data Stored!")
            else: self.override_player_hand_data()
        self.lock_input = False

    def gen_player_hand_data(self):
        self.player_turn_count += 1
        if self.debug_info: print(f"====================================================[TURN {self.player_turn_count}]====================================================")
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
            card = self.CardCore.compare_text_with_description_return_highest(screenshot_text)
            if self.debug_info: print(card)
            self.CardStorageCore.add_card_to_area(CardAreas.Player_Hand, card)

    def override_player_hand_data(self):
        for card in self.CardStorageCore.return_card_area(CardAreas.Player_Hand):
            if input(f"Override card {card['CardName']}? (Y/N) ").lower() == "y":
                new_card = self.CardCore.return_card_from_name(input("New Card: "))
                if new_card is None: continue
                index = self.CardStorageCore.return_index_of_object(CardAreas.Player_Hand, card)
                self.CardStorageCore.set_card_at_index(CardAreas.Player_Hand, index, new_card)

    #todo Decide what position to summon
    #todo Decide what star to summon with
    def gen_best_card_to_play_for_player(self):
        if self.debug_info: print("[STARTING BEST CARD GEN]")
        player_hand = self.CardStorageCore.return_card_area(CardAreas.Player_Hand)
        highest_card, is_fusion = self.CardCore.return_best_option_for_player(player_hand, SearchMethod.ATK)
        if self.debug_info: print(f"{highest_card},{is_fusion}")
        if is_fusion:
            screen_pos = self.ScreenGrabController.convert_pos(pos_x=30, pos_y=30)
            self.InputController.click_pos(posx=screen_pos[0], posy=screen_pos[1])
            index_a, index_b, card_a, card_b = self.CardCore.return_all_fusion_materials_from_players_hand(highest_card, player_hand)
            self.CursorCore.set_cursor_position(index_a)
            self.InputController.up_click_button()
            self.CursorCore.set_cursor_position(index_b)
            self.InputController.up_click_button()
            self.InputController.click_button('z', delay=1)
            self.InputController.click_button('z', delay=4)
            self.InputController.click_button('z', delay=1)
            highest_card['Position'] = CardPositions.ATK.name
            self.CardStorageCore.remove_card_from_area(CardAreas.Player_Hand, card_a)
            self.CardStorageCore.remove_card_from_area(CardAreas.Player_Hand, card_b)
            self.CardStorageCore.add_card_to_area(CardAreas.Player_Monsters, highest_card)
        else:
            screen_pos = self.ScreenGrabController.convert_pos(pos_x=30, pos_y=30)
            self.InputController.click_pos(posx=screen_pos[0], posy=screen_pos[1])
            card_index = self.CardStorageCore.return_index_of_object(CardAreas.Player_Hand, highest_card)
            self.CursorCore.set_cursor_position(card_index)
            self.InputController.click_button('z', delay=1)
            self.InputController.right_click_button()
            self.InputController.click_button('z', delay=1)
            self.InputController.click_button('z', delay=1)
            self.InputController.click_button('z', delay=1)
            highest_card['Position'] = CardPositions.ATK.name
            self.CardStorageCore.remove_card_from_area(CardAreas.Player_Hand, highest_card)
            self.CardStorageCore.add_card_to_area(CardAreas.Player_Monsters, highest_card)

    #todo find a way to tell what position the creature is in
    def gather_board_info_for_ai(self):
        if self.debug_info: print("[STARTING GATHER BOARD INFO]")
        screen_pos = self.ScreenGrabController.convert_pos(pos_x=30, pos_y=30)
        self.InputController.click_pos(posx=screen_pos[0], posy=screen_pos[1])
        self.CursorCore.default_cursor()
        self.InputController.up_click_button()
        for i in range(0, 5, 1):
            self.CursorCore.set_cursor_position(i)
            screenshot = self.ScreenGrabController.take_screenshot()
            if not self.ScreenGrabController.does_image_contain_more_than(screenshot.crop((47, 675, 848, 734)), [(0, 0, 0), (3.1, 3.1, 3.1), (8, 8, 8)]):
                if self.debug_info: print("Empty Space!")
            elif not self.ScreenGrabController.does_image_contain_more_than(screenshot.crop((47, 675, 583, 734)), [(0, 0, 0), (3.1, 3.1, 3.1), (8, 8, 8)]):
                self.CardStorageCore.add_card_to_area(CardAreas.Other_Monsters, {
                    "CardID": "000",
                    "CardName": "BlankCard",
                    "CardATK": "0",
                    "CardDEF": "0",
                    "Position": CardPositions.DEF.name
                })
            else:
                if self.debug_info: print("Found real card in other zone")

    #todo highest stat is based on atk, change to update when def detection is implemented
    def atk_player_monsters(self):
        creatures_attacked = []
        screen_pos = self.ScreenGrabController.convert_pos(pos_x=30, pos_y=30)
        self.InputController.click_pos(posx=screen_pos[0], posy=screen_pos[1])
        self.CursorCore.default_cursor()
        self.InputController.down_click_button(delay=1)
        if self.debug_info: print("[STARTING ATK PLAYER MONSTERS]")
        for our_monster in self.CardStorageCore.return_card_area(CardAreas.Player_Monsters):
            if our_monster in creatures_attacked: continue
            if our_monster['Position'] == CardPositions.DEF.name: continue
            highest_atk_monster = self.CardStorageCore.return_highest_atk_card_from_area(CardAreas.Other_Monsters)
            if highest_atk_monster is None:
                self.InputController.click_button('z', delay=1)
                self.InputController.click_button('z', delay=5)
                self.InputController.right_click_button()
            elif int(our_monster['CardATK']) > int(highest_atk_monster['CardATK']):
                self.InputController.click_button('z', delay=1)
                card_index = self.CardStorageCore.return_index_of_object(CardAreas.Other_Monsters, highest_atk_monster)
                print(self.CursorCore.cursor_position)
                self.CursorCore.set_cursor_position(new_cursor_position=4 - card_index)
                self.InputController.click_button('z', delay=5)
                self.CardStorageCore.remove_card_from_area(CardAreas.Other_Monsters, highest_atk_monster)
                creatures_attacked.append(our_monster)
                self.InputController.right_click_button()
        print("Looped Through All Monsters")


    def end_turn(self):
        if self.debug_info: print("[STARTING END TURN]")
        screen_pos = self.ScreenGrabController.convert_pos(pos_x=30, pos_y=30)
        self.InputController.click_pos(posx=screen_pos[0], posy=screen_pos[1])
        self.InputController.enter_click_button()

    def end_program(self):
        if self.debug_info: print("[STARTING END PROGRAM]")