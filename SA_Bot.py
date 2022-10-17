from Bot import Bot
from GameAction import GameAction
from GameState import GameState
import random
import numpy as np
import time
import copy

class SA_Bot(Bot):
    def __init__(self) -> None:
        super().__init__()
        self.__BOT_TIMEOUT_SECOND = 5
        self.__INIT_TEMP = 100

    """ Methods for returning a marking action over given GameState """
    def get_action(self, state: GameState) -> GameAction:
        iteration = 0
        current_temp = self.__INIT_TEMP
        start_time = time.time()

        current_marking = self.__random_marking(state)
        current_state = self.__modify_state(state, current_marking)
        
        while (time.time() - start_time < self.__BOT_TIMEOUT_SECOND):
            iteration += 1
            current_temp = self.__cooling_temp(current_temp, iteration)
            if (current_temp == 0):
                return current_marking

            neighbor_marking = self.__random_marking(current_state)
            neighbor_state = self.__modify_state(current_state, neighbor_marking)

            delta_E = self.__obj_func(neighbor_state, neighbor_marking) - self.__obj_func(current_state, current_marking)
            is_accept = 2.71828**(delta_E/current_temp) > random.randrange(0, 1)  
            if (delta_E > 0 or is_accept):
                current_marking = neighbor_marking
        
        return current_marking

    def __modify_state(self, state: GameState, action: GameAction) -> GameState:
        modfied_state = copy.copy(state)
        x = action.position[0]
        y = action.position[1]

        if (action.action_type == "row"):
            modfied_state.row_status[y][x] = 1
        elif (action.action_type == "col"):
            modfied_state.col_status[y][x] = 1

        return modfied_state

    def __random_marking(self, state: GameState) -> GameAction:
        all_row_marked = np.all(state.row_status == 1)
        all_col_marked = np.all(state.col_status == 1)

        if not (all_row_marked or all_col_marked):
            return self.__get_random_marking(state)
        elif all_row_marked:
            return self.__get_random_col_marking(state)
        else:
            return self.__get_random_row_marking(state)

    def __get_random_marking(self, state: GameState) -> GameAction:
        if random.random() < 0.5:
            return self.__get_random_row_marking(state)
        else:
            return self.__get_random_col_marking(state)

    def __get_random_row_marking(self, state: GameState) -> GameAction:
        position = self.__get_random_position_with_zero_value(state.row_status)
        return GameAction("row", position)

    def __get_random_col_marking(self, state: GameState) -> GameAction:
        position = self.__get_random_position_with_zero_value(state.col_status)
        return GameAction("col", position)

    def __get_random_position_with_zero_value(self, matrix: np.ndarray):
        [ny, nx] = matrix.shape

        x = -1
        y = -1
        valid = False
        
        while not valid:
            x = random.randrange(0, nx)
            y = random.randrange(0, ny)
            valid = matrix[y, x] == 0
        
        return (x, y)

    """ Cooling Schedule """
    def __cooling_temp(self, current_temp, iteration):
        # fast simulated annealing. Trial and error needed
        return current_temp/iteration

    """ Heuristic Functions """
    def __obj_func(self, modified_state: GameState, marked_position: GameAction):
        total_score = 0
        pass

    def __box_eval(self, modified_state: GameState, marked_position: GameAction, is_extra_turn: bool = False):
        pass