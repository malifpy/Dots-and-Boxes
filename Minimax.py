from typing import List
from GameAction import *
from GameState import *
from Node import *
from Bot import *
import numpy as np
import time

class MinimaxBot(Bot): 
    def __init__(self, player1 = False):
        self.__BOT_TIMEOUT_SECOND = 5
        self.player1 = player1
        
    def get_position(self, posisi = np.ndarray) -> list[Tuple[int, int]]:
        #untuk mendapatkan posisi yang belum di mark (status = 0)
        [y,x] = posisi.shape
        posisiKosong : list[Tuple[int,int]] = []
        for j in range(y):
            for i in range(x):
                if(posisi[j,i] == 0):
                    posisiKosong.append((i,j))
                
        return posisiKosong
    
    def get_list_action(self, state : GameState) -> List[GameAction]:
        #digunakan untuk melist aksi yang bisa dilakukan, melist aksi pada yg belum di mark
        row = self.get_position(state.row_status)
        col = self.get_position(state.col_status)
        
        list_aksi : List[GameAction] = []
        
        for posisi in row:
            list_aksi.append(GameAction("row", posisi))
        for posisi in col:
            list_aksi.append(GameAction("col", posisi))
            
        return list_aksi
        
    def minimax(self, state : GameState, alpha : int , beta : int, depth : int = 0) -> int:
        start = time.time()
        Max = -99999
        Min = 99999
        
        if ((state.col_status == 1).all() and (state.col_status == 1).all() or depth >= 3):
            return self.utilitidValue(state)
        
        while(time.time() - start <= self.__BOT_TIMEOUT_SECOND):
            if (self.player1 ^ state.player1_turn) #turn player 1
                list_aksi = self.get_list_action(state)
                for i in list_aksi:
                    value = self.minimax(self.get_next_turn(state,i), alpha, beta, depth + 1) # harusnya i nya ada fungsi gtu tpi buat cari new statenya
                    if(value > Max):
                        Max = value
                    if(Max > alpha):
                        alpha = Max
                    if(beta <= alpha):
                        break
                return Max;
            else:
                list_aksi = self.get_list_action(state)
                for i in list_aksi:
                    value = self.minimax(self.get_next_turn(state,i), alpha, beta, depth +1) # harusnya i nya ada fungsi gtu tpi buat cari new statenya
                    if(value < Min):
                        Min = value
                    if(Min < beta):
                        beta = Min
                    if(beta <= alpha):
                        break;
                return Min;
            
    def get_action(self, state : GameState) -> GameAction: # akan menghasilkan pergerakan yang best, sesuai dengan algoritma minimax
        pass
    
    def utilitidValue(self, state : GameState) -> int:
        pass
    
    def get_next_turn(self, state: GameState, action: GameAction) -> GameState:
        pass