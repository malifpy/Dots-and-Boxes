from typing import Tuple
from GameAction import GameAction
from GameState import GameState
from Heuristic_Value import *
from Support_Function import *
import numpy as np

""" Heuristic Functions """
def get_ud_status_row(state: GameState, position: Tuple[int, int]):
    """
    Mendapatkan status dari kotak diatas dan dibawah mark row
    """
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
    
def get_lr_status_col(state: GameState, position: Tuple[int, int]):
    """
    Mendapatkan status dari kotak di kiri dan di kanan mark col
    """
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
    
def has_extra_move(state: GameState, action: GameAction):
    """
    Menentukan apakah player akan mendapatkan extra turn ketika
    melakukan aksi action pada kondisi state 
    """
    if action.action_type == "row":
        adjacent_status = get_ud_status_row(state, action.position)
    else:
        adjacent_status = get_lr_status_col(state, action.position)
    return np.any(np.absolute(adjacent_status) + 1 == 4)
def box_eval(box_status: int, is_extra_turn: bool = False):
    """
    Menilai tiap kotak
    """
    if box_status == 4:
        return 2
    elif box_status == -4:
        return -2
    elif box_status == 0:
        return 0
    else:
        if box_status == 1:
            return (int(is_extra_turn) * 2 - 1) * -1
        elif box_status == 2:
            return (int(is_extra_turn) * 2 - 1) * 1
        else:
            return (int(is_extra_turn) * 2 - 1) * 2
    
def obj_func(original_state: GameState, marked_position: GameAction):
    """
    Menjumlahkan nilai tiap kotak
    """
    has_extra_turn = has_extra_move(original_state, marked_position)
    total_score = 0
    for box_status_row in original_state.board_status:
        for box_status in box_status_row:
            total_score += box_eval(box_status, has_extra_turn)
    return total_score