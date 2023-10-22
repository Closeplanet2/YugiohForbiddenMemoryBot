from enum import Enum

class StateList(Enum):
    STARTING = 0
    GEN_PLAYER_HAND = 1
    FIND_BEST_CARD_TO_PLAY = 2
    GEN_AI_BOARD = 3
    COMBAT = 4
    END_TURN = 5
    END_PROGRAM = 6

class StateMachine:
    def __init__(self, debug_info=True):
        self.current_state = StateList.STARTING
        self.callback_functions = {}
        self.callback_functions[StateList.STARTING.name] = []
        self.callback_functions[StateList.GEN_PLAYER_HAND.name] = []
        self.callback_functions[StateList.FIND_BEST_CARD_TO_PLAY.name] = []
        self.callback_functions[StateList.GEN_AI_BOARD.name] = []
        self.callback_functions[StateList.COMBAT.name] = []
        self.callback_functions[StateList.END_TURN.name] = []
        self.callback_functions[StateList.END_PROGRAM.name] = []
        self.debug_info = debug_info

    def add_callback_function(self, state, callback_function):
        if state is None or callback_function is None: return
        if self.debug_info: print("Added callback function!")
        self.callback_functions[state.name].append(callback_function)

    async def trigger_callback_functions(self, state):
        if len(self.callback_functions[state.name]) <= 0: return False
        for callback_function in self.callback_functions[state.name]:
            await callback_function()
        return True

    async def trigger_state_machine(self, loop_once=False, ignore_gather_info=True, ignore_combat=False):
        if self.current_state is StateList.STARTING: self.current_state = StateList.GEN_PLAYER_HAND
        elif self.current_state is StateList.GEN_PLAYER_HAND: self.current_state = StateList.FIND_BEST_CARD_TO_PLAY
        elif self.current_state is StateList.FIND_BEST_CARD_TO_PLAY:
            if ignore_gather_info:
                if ignore_combat: self.current_state = StateList.END_TURN
                else: self.current_state = StateList.COMBAT
            else: self.current_state = StateList.GEN_AI_BOARD
        elif self.current_state is StateList.GEN_AI_BOARD:
            if ignore_combat: self.current_state = StateList.END_TURN
            else: self.current_state = StateList.COMBAT
        elif self.current_state is StateList.COMBAT: self.current_state = StateList.END_TURN
        elif self.current_state is StateList.END_TURN:
            if loop_once: self.current_state = StateList.END_PROGRAM
            else: self.current_state = StateList.GEN_PLAYER_HAND
        await self.trigger_callback_functions(self.current_state)