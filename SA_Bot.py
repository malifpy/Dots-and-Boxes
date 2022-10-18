from typing import Tuple
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
        self.__ROWCOL_PROBABILITY = 0.43

    def get_action(self, state: GameState) -> GameAction:
        iteration = 0
        current_temp = self.__INIT_TEMP
        start_time = time.time()

        current_marking = self.__global_random_marking(state)
        current_state = self.__modify_state(state, current_marking)
        
        while (time.time() - start_time < self.__BOT_TIMEOUT_SECOND):
            iteration += 1
            print(iteration)
            current_temp = self.__cooling_temp(current_temp)
            if (current_temp == 0):
                return current_marking

            neighbor_marking = self.__local_random_marking(state, current_marking)
            neighbor_state = self.__modify_state(state, neighbor_marking)
            E_neighbor = self.__obj_func(neighbor_state, neighbor_marking)
            E_current = self.__obj_func(current_state, current_marking)
            
            delta_E = E_neighbor - E_current
            if (delta_E > 0):
                current_marking = neighbor_marking
            elif 2.71828 ** round(delta_E / current_temp, 3) > random.randrange(0, 1):
                current_marking = neighbor_marking
        
        return current_marking

    def __modify_state(self, state: GameState, action: GameAction) -> GameState:
        modified_state = copy.deepcopy(state)
        (col, row) = action.position

        if (action.action_type == "row"):
            modified_state.row_status[row][col] = 1
        elif (action.action_type == "col"):
            modified_state.col_status[row][col] = 1

        return modified_state

    def __global_random_marking(self, state: GameState) -> GameAction:
        all_row_marked = self.__is_all_marked(state.row_status)
        all_col_marked = self.__is_all_marked(state.col_status)

        if not (all_row_marked or all_col_marked):
            return self.__global_get_random_marking(state)
        elif all_row_marked:
            return self.__global_random_col_marking(state)
        else:
            return self.__global_random_row_marking(state)

    def __global_get_random_marking(self, state: GameState) -> GameAction:
        if random.random() < 0.5:
            return self.__global_random_row_marking(state)
        else:
            return self.__global_random_col_marking(state)

    def __global_random_row_marking(self, state: GameState) -> GameAction:
        position = self.__global_random_position_with_zero_value(state.row_status)
        return GameAction("row", position)

    def __global_random_col_marking(self, state: GameState) -> GameAction:
        position = self.__global_random_position_with_zero_value(state.col_status)
        return GameAction("col", position)

    def __global_random_position_with_zero_value(self, matrix_status: np.ndarray):
        [ny, nx] = matrix_status.shape

        x = -1
        y = -1
        valid = False
        
        while not valid:
            x = random.randrange(0, nx)
            y = random.randrange(0, ny)
            valid = matrix_status[y, x] == 0
        
        return (x, y)

    def __local_random_marking(self, state: GameState, marking_ref: GameAction) -> GameAction:
        """
        Return any neighbor-marking action available of current_marking.

        Neighbor-marking of current_marking is defined as legal clockwise and counterclockwise rotation "sweeping" areas 
        """
        if (marking_ref.action_type == "row"):
            if (random.random() >= self.__ROWCOL_PROBABILITY):
                return self.__local_random_row_marking(state.row_status, marking_ref)
            else:
                return self.__local_random_col_marking(state.col_status, marking_ref)         

        else:
            if (random.random() >= self.__ROWCOL_PROBABILITY):
                return self.__local_random_col_marking(state.col_status, marking_ref)
            else:
                return self.__local_random_row_marking(state.row_status, marking_ref)

    def __local_random_row_marking(self, row_state: np.ndarray, marking_ref: GameAction):
        (pos_x, pos_y) = copy.deepcopy(marking_ref.position)

        if (marking_ref.action_type == "row"):
            init_x = pos_x - 1 if (pos_x - 1) >= 0 else 0
            max_x = pos_x + 1 if (pos_x + 1) <= 2 else 2
            init_y = pos_y - 1 if (pos_y - 1) >= 0 else 0
            max_y = pos_y + 1 if (pos_y + 1) <= 3 else 3
        else:
            init_x = pos_x - 1 if (pos_x - 1) >= 0 else 0
            max_x = pos_x if pos_x <= 2 else 2
            init_y = pos_y - 1 if (pos_y - 1) >= 0 else 0
            max_y = pos_y + 2 if (pos_y + 2) <= 3 else 3
            
        if (self.__is_all_marked(row_state[init_y: max_y + 1, init_x: max_x + 1] == 1)):
            return marking_ref

        valid = False
        while not valid:
            pos_x = random.randint(init_x, max_x)
            pos_y = random.randint(init_y, max_y)
            valid = row_state[pos_y, pos_x] == 0
    
        return GameAction("row", (pos_x, pos_y))

    def __local_random_col_marking(self, col_state: np.ndarray, marking_ref: GameAction):
        (pos_x, pos_y) = copy.deepcopy(marking_ref.position)

        if (marking_ref.action_type == "row"):
            init_x = pos_x - 1 if (pos_x - 1) >= 0 else 0
            max_x = pos_x + 2 if (pos_x + 2) <= 3 else 3
            init_y = pos_y - 1 if (pos_y - 1) >= 0 else 0
            max_y = pos_y if pos_y <= 2 else 2
        else:
            init_x = pos_x - 1 if (pos_x - 1) >= 0 else 0
            max_x = pos_x + 1 if (pos_x + 1) <= 3 else 3
            init_y = pos_y - 1 if (pos_y - 1) >= 0 else 0
            max_y = pos_y + 1 if (pos_y + 1) <= 2 else 2
        
        if (self.__is_all_marked(col_state[init_y: max_y + 1, init_x: max_x + 1] == 1)):
            return marking_ref
        
        valid = False
        while not valid:
            pos_x = random.randint(init_x, max_x)
            pos_y = random.randint(init_y, max_y)
            valid = col_state[pos_y, pos_x] == 0
    
        return GameAction("col", (pos_x, pos_y))

    def __is_all_marked(self, matrix_status: np.ndarray):
        return np.all(matrix_status == 1)

    """ Cooling Schedule """
    def __cooling_temp(self, current_temp):
        return current_temp / 2

    """ Heuristic Functions """
    def __get_ud_status_row(self, state: GameState, position: Tuple[int, int]):
        [max_row, _] = state.board_status.shape
        (p_col, p_row) = position

        if (p_row - 1 < 0):
            up_status = np.nan
        else:
            up_status = state.board_status[p_row - 1][p_col]

        if (p_row >= max_row):
            down_status = np.nan
        else:
            down_status = state.board_status[p_row][p_col]

        return np.array([up_status, down_status])

    def __get_lr_status_col(self, state: GameState, position: Tuple[int, int]):
        [_, max_col] = state.board_status.shape
        (p_col, p_row) = position

        if (p_col - 1 < 0):
            left_status = np.nan
        else:
            left_status = state.board_status[p_row][p_col - 1]

        if (p_col >= max_col):
            right_status = np.nan
        else:
            right_status = state.board_status[p_row][p_col]
            
        return np.array([left_status, right_status])

    def __has_extra_move(self, state: GameState, action: GameAction):
        if action.action_type == "row":
            adjacent_status = self.__get_ud_status_row(state, action.position)
        else:
            adjacent_status = self.__get_lr_status_col(state, action.position)

        return np.any(np.absolute(adjacent_status) + 1 == 4)

    def __box_eval(self, box_status: int, is_extra_turn: bool = False):
        if box_status == 4:
            return 2
        elif box_status == -4:
            return 2
        elif box_status == 0:
            return 0
        else:
            box_side = abs(box_status)
            if box_side == 1:
                return -1
            elif box_side == 2:
                return -1
            else:
                return (int(is_extra_turn) * 2 - 1) * 2

    def __obj_func(self, modified_state: GameState, marked_position: GameAction):
        has_extra_turn = self.__has_extra_move(modified_state, marked_position)
        total_score = 0
        for box_status_row in modified_state.board_status:
            for box_status in box_status_row:
                total_score += self.__box_eval(box_status, has_extra_turn)
        return total_score
