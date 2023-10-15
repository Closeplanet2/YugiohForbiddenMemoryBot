from enum import Enum

class States(Enum):
    LOADING = 0
    GEN_HAND_DATA = 1
    GEN_BEST_CARD_TO_PLAY = 2
    GATHER_BOARD_INFO = 3
    ATK_PLAYERS_MONSTERS = 4
    END_TURN = 5
    END_PROGRAM = 6

class StateCore:
    def __init__(self):
        self.current_state = States.LOADING

    def trigger_state_machine(self, loop_once=False, ignore_gather_info=True, ignore_combat=True):
        if self.current_state is States.LOADING: self.current_state = States.GEN_HAND_DATA
        elif self.current_state is States.GEN_HAND_DATA: self.current_state = States.GEN_BEST_CARD_TO_PLAY
        elif self.current_state is States.GEN_BEST_CARD_TO_PLAY:
            if ignore_gather_info:
                if ignore_combat: self.current_state = States.END_TURN
                else: self.current_state = States.ATK_PLAYERS_MONSTERS
            else: self.current_state = States.GATHER_BOARD_INFO
        elif self.current_state is States.GATHER_BOARD_INFO:
            if ignore_combat: self.current_state = States.END_TURN
            else: self.current_state = States.ATK_PLAYERS_MONSTERS
        elif self.current_state is States.ATK_PLAYERS_MONSTERS: self.current_state = States.END_TURN
        elif self.current_state is States.END_TURN:
            if loop_once: self.current_state = States.END_PROGRAM
            else: self.current_state = States.GEN_HAND_DATA
        return self.current_state