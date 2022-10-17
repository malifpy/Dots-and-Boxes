from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from typing import Tuple
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

        __debug_max_delta = 0
        
        while (time.time() - start_time < self.__BOT_TIMEOUT_SECOND):
            iteration += 1
            current_temp = self.__cooling_temp(current_temp, iteration)
            if (current_temp == 0):
                return current_marking

            neighbor_marking = self.__random_marking(state)
            neighbor_state = self.__modify_state(state, neighbor_marking)

            # delta_E = self.__obj_func(neighbor_state, neighbor_marking) - self.__obj_func(current_state, current_marking)
            # print("call neighbor")
            E_neighbor = self.__obj_func(neighbor_state, neighbor_marking)
            # print("call current")
            E_current = self.__obj_func(current_state, current_marking)
            delta_E = E_neighbor - E_current
            # is_accept = 2.71828 ** round(- delta_E / current_temp, 3) > random.randrange(0, 1)  
            if delta_E > __debug_max_delta:
                __debug_max_delta = delta_E
            # print(iteration, neighbor_marking, state.board_status, delta_E)

            if (delta_E > 0):
                current_marking = neighbor_marking
            elif 2.71828 ** round(delta_E / current_temp, 3) > random.randrange(0, 1):
                current_marking = neighbor_marking
        
        return current_marking

    def __modify_state(self, state: GameState, action: GameAction) -> GameState:
        modfied_state = copy.deepcopy(state)
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
        # return current_temp/iteration
        return current_temp / 2

    """ Heuristic Functions """
    def __get_ud_status_row(self, state: GameState, position: Tuple[int, int]):
        [max_y, max_x] = state.board_status.shape
        (px, py) = position
        # print(position)
        if (py - 1 < 0):
            up_status = np.nan
        else:
            up_status = state.board_status[py - 1][px]

        if (py >= max_y):
            down_status = np.nan
        else:
            down_status = state.board_status[py][px]

        # print("status row", up_status, down_status)
        return np.array([up_status, down_status])

    def __get_lr_status_col(self, state: GameState, position: Tuple[int, int]):
        [max_y, max_x] = state.board_status.shape
        (px, py) = position
        # print(position)
        if (px - 1 < 0):
            left_status = np.nan
        else:
            left_status = state.board_status[py][px - 1]

        if (px >= max_x):
            right_status = np.nan
        else:
            right_status = state.board_status[py][px]

        # print("status col", left_status, right_status)
        return np.array([left_status, right_status])

    def __has_extra_move(self, state: GameState, action: GameAction):
        # print(action)
        if action.action_type == "row":
            adjacent_status = self.__get_ud_status_row(state, action.position)
        else:
            adjacent_status = self.__get_lr_status_col(state, action.position)

        # print(np.any(np.absolute(adjacent_status) + 1 == 4))
        return np.any(np.absolute(adjacent_status) + 1 == 4)

    def __box_eval(self, box_status: int, is_extra_turn: bool = False):
        if box_status == 4:
            return 2
        elif box_status == -4:
            return 2
        elif box_status == 0:
            return 0
        elif abs(box_status) == 1:
            return -1
        elif abs(box_status) == 2:
            return 1
        else:
            return (int(is_extra_turn) * 2 - 1) * 2

    def __obj_func(self, modified_state: GameState, marked_position: GameAction):
        # print(marked_position)
        has_extra_turn = self.__has_extra_move(modified_state, marked_position)
        total_score = 0
        for box_status_row in modified_state.board_status:
            for box_status in box_status_row:
                total_score += self.__box_eval(box_status, has_extra_turn)
        return total_score
