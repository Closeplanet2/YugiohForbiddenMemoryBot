from CORES.TkinterController import TkinterController, DestructionStage
from CORES.ScreenGrabController import ScreenGrabController
from CORES.InputController import InputController
from CORES.TextController import TextController
from CORES.ThreadController import ThreadController
from GAME_CORE.GameSettings import GameSettings
from GAME_CORE.CardStorageCore import CardStorageCore, CardAreas
from GAME_CORE.StateMachine import StateMachine, StateList
from GAME_CORE.CursorCore import CursorCore
from GAME_CORE.CardCore import CardCore, PlayStyle, CardType, CardSign, CardLocation, CardPositions
import asyncio

class GameCore:
    def __init__(self):
        self.GameSettings = GameSettings()
        self.TkinterController = TkinterController(debug_info=self.GameSettings.debug_info)
        self.ScreenGrabController = ScreenGrabController("RetroArch Beetle PSX HW 0.9.44.1 88929ae", debug_info=self.GameSettings.debug_info)
        self.InputController = InputController(debug_info=self.GameSettings.debug_info)
        self.InputController.listen_for_keyboard(on_press=self.callback_on_press, on_release=self.callback_on_release)
        self.CardStorageCore = CardStorageCore(debug_info=self.GameSettings.debug_info)
        self.CardStorageCore.add_callback_function(self.callback_card_changed_in_area)
        self.CardCore = CardCore(debug_info=self.GameSettings.debug_info)
        self.TextController = TextController()
        self.StateMachine = StateMachine(debug_info=self.GameSettings.debug_info)
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

    def callback_on_press(self, key):
        try:
            if key.char == '9':
                ThreadController(max_threads=1).load_start(self.callback_next_state_button, daemon=True)
            elif key.char == '0':
                ThreadController(max_threads=1).load_start(self.callback_override_player_data_callback, daemon=True)
        except AttributeError:
            pass

    def callback_on_release(self, key):
        pass

    def callback_left_click_button(self, current_cursor, delay):
        self.InputController.left_click_button(delay=delay)

    def callback_right_click_button(self, current_cursor, delay):
        self.InputController.right_click_button(delay=delay)

    def callback_next_state_button(self, thread_index, args):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.StateMachine.trigger_state_machine(loop_once=False, ignore_gather_info=self.player_turn_count <= 0, ignore_combat=self.player_turn_count <= 0))
        loop.close()

    def callback_override_player_data_callback(self, thread_index, args):
        if self.lock_input: return
        self.lock_input = True
        if input("Change Player Hand? (Y/N) ") == "y":
            if len(self.CardStorageCore.return_card_array_from_card_area(CardAreas.Player_Hand)) == 0:
                print("No Hand Data Stored!")
            else:
                self.override_player_hand_data()
        self.lock_input = False

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

    def override_player_hand_data(self):
        for card in self.CardStorageCore.return_card_array_from_card_area(CardAreas.Player_Hand):
            if input(f"Override card {card['CardName']}? (Y/N) ").lower() == "y":
                new_card = self.CardCore.return_card_from_name(input("New Card: "))
                if new_card is None: continue
                index = self.CardStorageCore.index_card_from_area(CardAreas.Player_Hand, card)
                self.CardStorageCore.set_card_at_index(CardAreas.Player_Hand, index, new_card)

    async def callback_find_best_card_to_play(self):
        if GameSettings.debug_info: print("[STARTING BEST CARD TO PLAY]")
        player_hand = self.CardStorageCore.return_card_array_from_card_area(CardAreas.Player_Hand)
        player_field = self.CardStorageCore.return_card_array_from_card_area(CardAreas.Player_Monsters)
        highest_card, card_type, play_style, card_sign, index_to_play = self.CardCore.return_best_option_for_player(
            player_hand=player_hand, player_field=player_field
        )
        if self.GameSettings.debug_info: print(f"{highest_card}, {card_type}, {play_style}")
        if card_type is CardType.FUSION_MONSTER:
            await self.play_fusion_monster(highest_card, card_type, play_style, card_sign, index_to_play)
        elif card_type is CardType.MONSTER:
            await self.play_monster(highest_card, card_type, play_style, card_sign, index_to_play)
        elif card_type is CardType.SPELL:
            self.play_spells(highest_card, card_type, play_style, card_sign, index_to_play)

    async def play_fusion_monster(self, highest_card, card_type, play_style, card_sign, index_to_play):
        self.click_screen()
        player_hand = self.CardStorageCore.return_card_array_from_card_area(CardAreas.Player_Hand)
        player_field = self.CardStorageCore.return_card_array_from_card_area(CardAreas.Player_Monsters)
        card_a_index, card_b_index, card_a_location, card_b_location, card_a, card_b = self.CardCore.return_all_fusion_materials_from_players_hand(highest_card, player_hand, player_field)

        if card_a_location is CardLocation.HAND:
            await self.CursorCore.set_cursor_position(card_a_index)
            self.InputController.up_click_button()

        if card_b_location is CardLocation.HAND:
            await self.CursorCore.set_cursor_position(card_b_index)
            self.InputController.up_click_button()

        self.InputController.click_button('z', hold_delay=1)
        await self.CursorCore.default_cursor()
        await self.CursorCore.set_cursor_position(index_to_play)
        self.InputController.click_button('z', hold_delay=4)

        # Assign the star sign
        if card_sign is CardSign.RANDOM:
            self.InputController.click_button('z', hold_delay=1)
        else:
            self.InputController.click_button('z', hold_delay=1)

        # Switch the card between def and atk
        if play_style is PlayStyle.FACE_UP_DEF or play_style is PlayStyle.FACE_DOWN_DEF:
             self.InputController.click_button('q', hold_delay=1)

        self.CardStorageCore.remove_card_from_area(CardAreas.Player_Hand, card_a)
        self.CardStorageCore.remove_card_from_area(CardAreas.Player_Hand, card_b)
        highest_card['Position'] = play_style.name
        self.CardStorageCore.add_card_to_area(CardAreas.Player_Monsters, highest_card)

    async def play_monster(self, highest_card, card_type, play_style, card_sign, index_to_play):
        self.click_screen()
        card_index = self.CardStorageCore.index_card_from_area(CardAreas.Player_Hand, highest_card)
        await self.CursorCore.default_cursor()
        await self.CursorCore.set_cursor_position(card_index)
        self.InputController.click_button('z', hold_delay=0.5)

        # Set if the card is face up or face down
        if play_style is PlayStyle.FACE_UP_ATK:
            self.InputController.right_click_button()
        elif play_style is PlayStyle.FACE_DOWN_ATK: pass
        else:
            self.InputController.right_click_button()

        self.InputController.click_button('z', hold_delay=1)
        await self.CursorCore.set_cursor_position(index_to_play)
        self.InputController.click_button('z', hold_delay=1)

        #Assign the star sign
        if card_sign is CardSign.RANDOM:
            self.InputController.click_button('z', hold_delay=1)
        else:
            self.InputController.click_button('z', hold_delay=1)

        #Switch the card between def and atk
        if play_style is PlayStyle.FACE_UP_DEF or play_style is PlayStyle.FACE_DOWN_DEF:
            self.InputController.click_button('q', hold_delay=1)

        self.CardStorageCore.remove_card_from_area(CardAreas.Player_Hand, highest_card)
        highest_card['Position'] = play_style.name
        self.CardStorageCore.add_card_to_area(CardAreas.Player_Monsters, highest_card)

    def play_spells(self, highest_card, card_type, play_style, card_sign, index_to_play):
        pass

    async def callback_gen_ai_board(self):
        if self.GameSettings.debug_info: print("[STARTING GATHER BOARD INFO]")
        self.click_screen()
        await self.CursorCore.default_cursor()
        self.InputController.up_click_button()
        for i in range(0, 5, 1):
            await self.CursorCore.set_cursor_position(i)
            screenshot = self.ScreenGrabController.take_screenshot()
            if not self.ScreenGrabController.does_image_contain_more_than(screenshot.crop((47, 675, 848, 734)), [(0, 0, 0), (3.1, 3.1, 3.1), (8, 8, 8)]):
                if self.GameSettings.debug_info:
                    print("Empty Space!")
            elif not self.ScreenGrabController.does_image_contain_more_than(screenshot.crop((47, 675, 583, 734)), [(0, 0, 0), (3.1, 3.1, 3.1), (8, 8, 8)]):
                self.CardStorageCore.add_card_to_area(CardAreas.Other_Monsters, {
                    "CardID": "000",
                    "CardName": "BlankCard",
                    "CardATK": "0",
                    "CardDEF": "0",
                    "Position": CardPositions.DEF.name
                })
            else:
                if self.GameSettings.debug_info:
                    print("Found real card in other zone")
        await self.CursorCore.default_cursor()
        self.InputController.down_click_button(delay=1)

    async def callback_combat(self):
        creatures_attacked = []
        self.click_screen()
        await self.CursorCore.default_cursor()
        if self.GameSettings.debug_info: print("[STARTING ATK PLAYER MONSTERS]")
        for our_monster in self.CardStorageCore.return_card_array_from_card_area(CardAreas.Player_Monsters):
            if our_monster in creatures_attacked: continue
            if our_monster['Position'] == PlayStyle.FACE_DOWN_DEF.name or our_monster['Position'] == PlayStyle.FACE_UP_DEF.name: continue
            highest_atk_monster = self.CardStorageCore.return_highest_atk_card_from_area(CardAreas.Other_Monsters)
            if highest_atk_monster is None:
                self.InputController.click_button('z', hold_delay=1)
                self.InputController.click_button('z', hold_delay=5)
                self.InputController.right_click_button()
            elif int(our_monster['CardATK']) > int(highest_atk_monster['CardATK']):
                self.InputController.click_button('z', hold_delay=1)
                card_index = self.CardStorageCore.index_card_from_area(CardAreas.Other_Monsters, highest_atk_monster)
                print(self.CursorCore.cursor_position)
                await self.CursorCore.set_cursor_position(new_cursor_position=4 - card_index)
                self.InputController.click_button('z', hold_delay=5)
                self.CardStorageCore.remove_card_from_area(CardAreas.Other_Monsters, highest_atk_monster)
                creatures_attacked.append(our_monster)
                self.InputController.right_click_button()

    async def callback_end_turn(self):
        if self.GameSettings.debug_info: print("[STARTING END TURN]")
        self.click_screen()
        self.InputController.enter_click_button()

    async def callback_end_program(self):
        pass

    def click_screen(self):
        screen_pos = self.ScreenGrabController.convert_pos(pos_x=30, pos_y=30)
        self.InputController.click_pos(posx=screen_pos[0], posy=screen_pos[1])