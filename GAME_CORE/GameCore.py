from CORES.TkinterController import TkinterController, DestructionStage
from CORES.ScreenGrabController import ScreenGrabController
from CORES.InputController import InputController
from CORES.TextController import TextController
from GAME_CORE.GameSettings import GameSettings
from GAME_CORE.CardStorageCore import CardStorageCore, CardAreas
from GAME_CORE.StateMachine import StateMachine, StateList
from GAME_CORE.CursorCore import CursorCore
from GAME_CORE.CardCore import CardCore
import asyncio

class GameCore:
    def __init__(self):
        self.GameSettings = GameSettings()
        self.TkinterController = TkinterController(debug_info=self.GameSettings.debug_info)
        self.ScreenGrabController = ScreenGrabController("RetroArch Beetle PSX HW 0.9.44.1 88929ae", debug_info=self.GameSettings.debug_info)
        self.InputController = InputController(debug_info=self.GameSettings.debug_info)
        self.CardStorageCore = CardStorageCore(debug_info=self.GameSettings.debug_info)
        self.CardStorageCore.add_callback_function(self.callback_card_changed_in_area)
        self.CardCore = CardCore(debug_info=self.GameSettings.debug_info)
        self.TextController = TextController()
        self.StateMachine = StateMachine(loop_once=False, ignore_gather_info=True, ignore_combat=False)
        self.StateMachine.add_callback_function(StateList.GEN_PLAYER_HAND, self.callback_gen_player_hand)
        self.StateMachine.add_callback_function(StateList.FIND_BEST_CARD_TO_PLAY, self.callback_find_best_card_to_play)
        self.StateMachine.add_callback_function(StateList.GEN_AI_BOARD, self.callback_gen_ai_board)
        self.StateMachine.add_callback_function(StateList.COMBAT, self.callback_combat)
        self.StateMachine.add_callback_function(StateList.END_TURN, self.callback_end_turn)
        self.StateMachine.add_callback_function(StateList.END_PROGRAM, self.callback_end_program)
        self.CursorCore = CursorCore(0, 4, self.callback_left_click_button, self.callback_right_click_button)
        self.lock_input = False
        self.player_turn_count = -1
        self.create_window()

    def create_window(self):
        self.TkinterController.create_window(
            function_thread_callback=self.function_thread_callback,
            wh=self.GameSettings.window_height, ww=self.GameSettings.window_width,
            wt=self.GameSettings.window_title, bg=self.GameSettings.window_background_color,
            update_gui_per_second=self.GameSettings.update_gui_per_second
        )

        self.TkinterController.add_callback_function(self.callback_create_player_hand_images)
        self.TkinterController.add_callback_function(self.callback_create_player_field_images)
        self.TkinterController.add_callback_function(self.callback_create_enemy_field_images)
        self.TkinterController.add_callback_function(self.TkinterController.destroy_widgets)

        self.TkinterController.add_label(
            text="Cards In Hand!", bg="#64FAFF", fg="#000000", w=int(self.GameSettings.window_width / 11), h=1, x_pos=0, y_pos=5,
            destroy_status=DestructionStage.DONT_DESTROY
        )
        self.TkinterController.add_label(
            text="Cards On Field!", bg="#64FAFF", fg="#000000", w=int(self.GameSettings.window_width / 11), h=1, x_pos=0, y_pos=175,
            destroy_status=DestructionStage.DONT_DESTROY
        )
        self.TkinterController.add_label(
            text="Cards On Enemy Field!", bg="#64FAFF", fg="#000000", w=int(self.GameSettings.window_width / 11), h=1, x_pos=0, y_pos=475,
            destroy_status=DestructionStage.DONT_DESTROY
        )

        self.TkinterController.add_button(
            text="Next State!", function_callback=self.callback_next_state_button, bg="#FF8181", fg="#000000",
            w=int(self.GameSettings.window_width / 11),
            h=1, x_pos=0, y_pos=862, destroy_status=DestructionStage.DONT_DESTROY
        )

        self.TkinterController.add_button(
            text="Override Data!", function_callback=self.callback_override_player_data_callback, bg="#FF8181", fg="#000000",
            w=int(self.GameSettings.window_width / 11),
            h=1, x_pos=0, y_pos=820, destroy_status=DestructionStage.DONT_DESTROY
        )

        self.TkinterController.start_window()

    def function_thread_callback(self):
        pass

    def callback_left_click_button(self, current_cursor, delay):
        self.InputController.left_click_button(delay=delay)

    def callback_right_click_button(self, current_cursor, delay):
        self.InputController.right_click_button(delay=delay)

    def callback_next_state_button(self, thread_index, args):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.StateMachine.trigger_state_machine())
        loop.close()

    def callback_override_player_data_callback(self, thread_index, args):
        pass

    def callback_create_player_hand_images(self, current_window):
        for i in range(0, 5, 1):
            card = self.CardStorageCore.return_card_from_index(CardAreas.Player_Hand, i)
            card_image = self.CardCore.return_card_image(card)
            self.TkinterController.add_image_as_grid(
                card_image=card_image, w=70, h=120, pos_x=5, pos_y=40, offset_x=79, offest_y=160, numx=5,
                numy=1, index=i, destroy_status=DestructionStage.DELAYED_DESTROY
            )

    def callback_create_player_field_images(self, current_window):
        for i in range(0, 5, 1):
            monster_card = self.CardStorageCore.return_card_from_index(CardAreas.Player_Monsters, i)
            monster_card_image = self.CardCore.return_card_image(monster_card)
            self.TkinterController.add_image_as_grid(
                card_image=monster_card_image, w=70, h=120, pos_x=5, pos_y=210, offset_x=79, offest_y=160, numx=5,
                numy=1, index=i, destroy_status=DestructionStage.DELAYED_DESTROY
            )
            spell_card = self.CardStorageCore.return_card_from_index(CardAreas.Player_Spells, i)
            spell_card_image = self.CardCore.return_card_image(spell_card)
            self.TkinterController.add_image_as_grid(
                card_image=spell_card_image, w=70, h=120, pos_x=5, pos_y=340, offset_x=79, offest_y=160, numx=5,
                numy=1, index=i, destroy_status=DestructionStage.DELAYED_DESTROY
            )

    def callback_create_enemy_field_images(self, current_window):
        for i in range(0, 5, 1):
            monster_card = self.CardStorageCore.return_card_from_index(CardAreas.Other_Monsters, i)
            monster_card_image = self.CardCore.return_card_image(monster_card)
            self.TkinterController.add_image_as_grid(
                card_image=monster_card_image, w=70, h=120, pos_x=5, pos_y=510, offset_x=79, offest_y=160, numx=5,
                numy=1, index=i, destroy_status=DestructionStage.DELAYED_DESTROY
            )
            spell_card = self.CardStorageCore.return_card_from_index(CardAreas.Other_Spells, i)
            spell_card_image = self.CardCore.return_card_image(spell_card)
            self.TkinterController.add_image_as_grid(
                card_image=spell_card_image, w=70, h=120, pos_x=5, pos_y=639, offset_x=79, offest_y=160, numx=5,
                numy=1, index=i, destroy_status=DestructionStage.DELAYED_DESTROY
            )

    def callback_card_changed_in_area(self, card_area, card_added, card):
        pass

    def callback_starting(self):
        print("Starting.......")

    async def callback_gen_player_hand(self):
        self.player_turn_count += 1
        if GameSettings.debug_info: print("[STARTING HAND GEN]")
        self.CardStorageCore.clear_card_area(CardAreas.Player_Hand, True)
        self.click_screen()
        self.InputController.click_button('x')
        await self.CursorCore.set_cursor_position(0, delay=0.5)
        for i in range(0, 5, 1):
            await self.CursorCore.set_cursor_position(i, delay=0.5)
            screenshot = self.ScreenGrabController.take_screenshot_and_crop(box=(35, 676, 588, 742))
            screenshot_text = self.TextController.image_to_text_pillow(pil_image=screenshot)
            highest_card = self.CardCore.find_card_with_closest_name(screenshot_text)
            if self.GameSettings.debug_info: print(f"Card Added To Hand: {highest_card}")
            self.CardStorageCore.add_card_to_area(CardAreas.Player_Hand, highest_card)

    async def callback_find_best_card_to_play(self):
        pass

    async def callback_gen_ai_board(self):
        pass

    async def callback_combat(self):
        pass

    async def callback_end_turn(self):
        pass

    async def callback_end_program(self):
        pass

    def click_screen(self):
        screen_pos = self.ScreenGrabController.convert_pos(pos_x=30, pos_y=30)
        self.InputController.click_pos(posx=screen_pos[0], posy=screen_pos[1])