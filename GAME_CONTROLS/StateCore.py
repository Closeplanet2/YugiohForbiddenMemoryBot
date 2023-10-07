from enum import Enum

class States(Enum):
    LOADING = 0
    GEN_HAND_DATA = 1
    GEN_BEST_CARD_TO_PLAY = 2
    GATHER_BOARD_INFO = 3
    END_TURN = 4
    END_PROGRAM = 5

class StateCore:
    def __init__(self):
        self.current_state = States.LOADING

    def trigger_state_machine(self, loop_once=False):
        if self.current_state is States.LOADING: self.current_state = States.GEN_HAND_DATA
        elif self.current_state is States.GEN_HAND_DATA: self.current_state = States.GEN_BEST_CARD_TO_PLAY
        elif self.current_state is States.GEN_BEST_CARD_TO_PLAY: self.current_state = States.GATHER_BOARD_INFO
        elif self.current_state is States.GATHER_BOARD_INFO: self.current_state = States.END_TURN
        elif self.current_state is States.END_TURN and loop_once: self.current_state = self.current_state = States.END_PROGRAM
        elif self.current_state is States.END_TURN and not loop_once: self.current_state = States.GEN_HAND_DATA
        return self.current_state