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
    def __init__(self, loop_once=False, ignore_gather_info=True, ignore_combat=False):
        self.current_state = StateList.LOADING
        self.callback_functions = {}
        self.callback_functions[StateList.STARTING.name] = []
        self.callback_functions[StateList.GEN_PLAYER_HAND.name] = []
        self.callback_functions[StateList.FIND_BEST_CARD_TO_PLAY.name] = []
        self.callback_functions[StateList.GEN_AI_BOARD.name] = []
        self.callback_functions[StateList.COMBAT.name] = []
        self.callback_functions[StateList.END_TURN.name] = []
        self.callback_functions[StateList.END_PROGRAM.name] = []
        self.loop_once = loop_once
        self.ignore_gather_info = ignore_gather_info
        self.ignore_combat = ignore_combat

    def add_callback_function(self, state, callback_function):
        if state is None or callback_function is None: return
        self.callback_functions[state.name].append(callback_function)

    def trigger_callback_functions(self, state):
        if len(self.callback_functions[state.name]) <= 0: return False
        for callback_function in self.callback_functions[state.name]:
            callback_function()
        return True

    def trigger_state_machine(self):
        if self.current_state is StateList.STARTING: self.current_state = StateList.GEN_PLAYER_HAND
        elif self.current_state is StateList.GEN_PLAYER_HAND: self.current_state = StateList.FIND_BEST_CARD_TO_PLAY
        elif self.current_state is StateList.FIND_BEST_CARD_TO_PLAY:
            if self.ignore_gather_info:
                if self.ignore_combat: self.current_state = StateList.END_TURN
                else: self.current_state = StateList.COMBAT
            else: self.current_state = StateList.GEN_AI_BOARD
        elif self.current_state is StateList.GEN_AI_BOARD:
            if self.ignore_combat: self.current_state = StateList.END_TURN
            else: self.current_state = StateList.COMBAT
        elif self.current_state is StateList.COMBAT: self.current_state = StateList.END_TURN
        elif self.current_state is StateList.END_TURN:
            if self.loop_once: self.current_state = StateList.END_PROGRAM
            else: self.current_state = StateList.GEN_PLAYER_HAND
        if not self.trigger_callback_functions(self.current_state): return self.current_state