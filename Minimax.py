from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from typing import Tuple
import copy
import numpy as np

#disini untuk kedalaman pertama menggunaakn minimax dan kedalaman berikutnya baru menggunakan alpha beta

class RandomBot(Bot):
    def __init__(self) -> None:
        super().__init__()
        print("Silakan masukkan kedalaman yang diinginkan (>0)")
        self.__kedalaman = int(input())
        while (self.__kedalaman <= 0 ) :
            print("Silakan masukkan kedalaman yang diinginkan")
            self.__kedalaman = int(input())

    def get_action(self, state: GameState) -> GameAction:
        #Menyimpan informasi parrent state (parent tree)
        parrent_state = (state)
        kedalaman = self.__kedalaman
        #Menyimpan informasi initial minimum score dan aksi yang nanti akan dikerjakan si bot
        minimum_score = 1000
        row_status = np.array(parrent_state.row_status)
        col_status = np.array(parrent_state.col_status)
        status = ""
        a = 0
        b = 0

        #untuk setiap row akan dicek mana yang belum diberi garis
        i = 0
        j = 0
        for i in range (4) :
            for j in range (3) :
                if ((row_status[i][j]) == 0): #jika ditemukan bagian belum digaris
                    #dicek kedalaman tree (ini bakal ada perubahan)
                    if kedalaman < 1 :
                        return (GameAction("row", (j,i)))
                    #simpan aksi yang dilakukan dan state setelah melakukan aski tersebut
                    temp_action = GameAction("row", (j,i)) #lakukan aksi pada bagian itu
                    temp_state_action = self.__modify_state(parrent_state, temp_action)
                    #lanjut ke kedalaman berikutnya
                    result = self.__maximum(temp_state_action, temp_action, kedalaman-1, minimum_score)
                    #akan dicek nilai costnya secara minimax
                    if minimum_score > result :
                        minimum_score = result
                        status = "row"
                        a = j
                        b = i

        #untuk setiap col akan dicek mana yang belum diberi garis
        i = 0
        j = 0
        for i in range (3) :
            for j in range (4) :
                if ((col_status[i][j]) == 0): #jika ditemukan bagian belum digaris
                    #dicek kedalaman tree (ini bakal ada perubahan)
                    if kedalaman < 1 :
                        return (GameAction("col", (j,i)))
                    #simpan aksi yang dilakukan dan state setelah melakukan aski tersebut
                    temp_action = GameAction("col", (j,i)) #lakukan aksi pada bagian itu
                    temp_state_action = self.__modify_state(parrent_state, temp_action)
                    result = self.__maximum(temp_state_action, temp_action, kedalaman-1, minimum_score)
                    #akan dicek nilai costnya secara minimax
                    if minimum_score > result :
                        minimum_score = result
                        status = "col"
                        a = j
                        b = i

        return (GameAction(status, (a,b)))

    def __maximum(self, state_action: GameState, action: GameAction, kedalaman, alpha):
        parrent_state = (state_action)

        if kedalaman == 0:
            cost = self.__obj_func(parrent_state, action)
            return (cost) #mengembalikan nilai cost pada keadaan sekarang

        #Menyimpan informasi initial maximum score dan aksi yang nanti akan dikerjakan si bot
        maximum_score = -1000
        row_status = np.array(parrent_state.row_status)
        col_status = np.array(parrent_state.col_status)

        #untuk setiap row akan dicek mana yang belum diberi garis
        i = 0
        j = 0
        for i in range (4) :
            for j in range (3) :
                if ((row_status[i][j]) == 0): #jika ditemukan bagian belum digaris
                    #simpan aksi yang dilakukan dan state setelah melakukan aski tersebut
                    temp_action = GameAction("row", (j,i)) #lakukan aksi pada bagian itu
                    temp_state_action = self.__modify_state(parrent_state, temp_action)
                    #lanjut ke kedalaman berikutnya
                    result = self.__minimum(temp_state_action, temp_action, kedalaman-1, maximum_score) #lakukan rekursif
                    #akan dicek nilai costnya secara alpha-beta pruning
                    if maximum_score < result :
                        maximum_score = result
                    if result > alpha :
                        return result

        #untuk setiap col akan dicek mana yang belum diberi garis
        i = 0
        j = 0
        for i in range (3) :
            for j in range (4) :
                if ((col_status[i][j]) == 0): #jika ditemukan bagian belum digaris
                    #simpan aksi yang dilakukan dan state setelah melakukan aski tersebut
                    temp_action = GameAction("col", (j,i)) #lakukan aksi pada bagian itu
                    temp_state_action = self.__modify_state(parrent_state, temp_action)
                    #lanjut ke kedalaman berikutnya
                    result = self.__minimum(temp_state_action, temp_action, kedalaman-1, maximum_score) #lakukan rekursif
                    #akan dicek nilai costnya secara alpha-beta pruning
                    if maximum_score < result :
                        maximum_score = result
                    if result > alpha :
                        return result

        return (maximum_score)

    def __minimum(self, state_action: GameState, action: GameAction, kedalaman, beta):
        parrent_state = (state_action)
        
        if kedalaman == 0:
            cost = self.__obj_func(parrent_state, action)
            return (cost) #mengembalikan nilai cost pada keadaan sekarang

        #Menyimpan informasi initial maximum score dan aksi yang nanti akan dikerjakan si bot
        minimum_score = 1000
        row_status = np.array(parrent_state.row_status)
        col_status = np.array(parrent_state.col_status)
        
        #untuk setiap row akan dicek mana yang belum diberi garis
        i = 0
        j = 0

        for i in range (4) :
            for j in range (3) :
                if ( (row_status[i][j]) == 0 ): #jika ditemukan bagian belum digaris
                    #simpan aksi yang dilakukan dan state setelah melakukan aski tersebut
                    temp_action = GameAction("row", (j,i)) #lakukan aksi pada bagian itu
                    temp_state_action = self.__modify_state(parrent_state, temp_action)
                    #lanjut ke kedalaman berikutnya
                    result = self.__maximum(temp_state_action, temp_action, kedalaman-1, minimum_score) #lakukan rekursif
                    #akan dicek nilai costnya secara alpha-beta pruning
                    if minimum_score > result :
                        minimum_score = result
                    if result < beta :
                        return result

        #untuk setiap col akan dicek mana yang belum diberi garis
        i = 0
        j = 0

        for i in range (3) :
            for j in range (4) :
                if ((col_status[i][j]) == 0): #jika ditemukan bagian belum digaris
                    #simpan aksi yang dilakukan dan state setelah melakukan aski tersebut
                    temp_action = GameAction("col", (j,i)) #lakukan aksi pada bagian itu
                    temp_state_action = self.__modify_state(parrent_state, temp_action)
                    #lanjut ke kedalaman berikutnya
                    result = self.__maximum(temp_state_action, temp_action, kedalaman-1, minimum_score) #lakukan rekursif
                    #akan dicek nilai costnya secara alpha-beta pruning
                    if minimum_score > result :
                        minimum_score = result
                    if result < beta :
                        return result

        return (minimum_score)

    def __modify_state(self, state: GameState, action: GameAction) -> GameState:
        modified_state = (state)
        (col, row) = action.position

        if (action.action_type == "row"):
            modified_state.row_status[row][col] = 1
        elif (action.action_type == "col"):
            modified_state.col_status[row][col] = 1

        return modified_state

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
            return -2
        elif box_status == 0:
            return 0
        else:
            box_side = abs(box_status)
            if box_side == 1:
                return -1
            elif box_side == 2:
                return 1
            else:
                return (int(is_extra_turn) * 2 - 1) * 2

    def __obj_func(self, modified_state: GameState, marked_position: GameAction):
        has_extra_turn = self.__has_extra_move(modified_state, marked_position)
        total_score = 0
        for box_status_row in modified_state.board_status:
            for box_status in box_status_row:
                total_score += self.__box_eval(box_status, has_extra_turn)
        return total_score
