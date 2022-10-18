from typing import List
from GameAction import *
from GameState import *
from Node import *
from Bot import *
import numpy as np
import time

class MinimaxBot(Bot): # masih rada ngaco karna belum kepikiran cara bikin treenya
    def __init__(self) -> None:
        super().__init__()
        self.__BOT_TIMEOUT_SECOND = 5
        
    def get_position(self, posisi = np.ndarray) -> list[Tuple[int, int]]:
        #untuk mendapatkan posisi yang belum di mark (status = 0)
        [y,x] = posisi.shape
        posisiKosong = list[Tuple[int,int]] = []
        for j in range(y):
            for i in range(x):
                if(posisi[j,i] == 0):
                    posisiKosong.append((i,j))
                
        return posisiKosong
    
    def get_list_action(self, state : GameState) -> List[GameAction]:
        #digunakan untuk melist aksi yang bisa dilakukan, melist aksi pada yg belum di mark
        row = self.get_position(state.row_status)
        col = self.get_position(state.col_status)
        
        list_aksi = List[GameAction] = []
        
        for posisi in row:
            list_aksi.append(GameAction("row", posisi))
        for posisi in col:
            list_aksi.append(GameAction("col", posisi))
            
        return list_aksi
        
    def minimax(self, state : GameState, alpha : int , beta : int, depth : int = 0, isMax : bool) -> int:
        start = time.time()
        Max = -99999
        Min = 99999
        
        if ((state.col_status == 1).all() and (state.col_status == 1).all() or depth >= 3):
            return utilitidValue(state)
        
        while(time.time() - start <= 5):
            if isMax: #turn player 1
                list_aksi = self.get_list_action(state)
                for i in list_aksi:
                    value = self.minimax(i, alpha, beta, depth - 1, isMax) # harusnya i nya ada fungsi gtu tpi buat cari new statenya
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
                    value = self.minimax(i, alpha, beta, depth - 1, isMax) # harusnya i nya ada fungsi gtu tpi buat cari new statenya
                    if(value < Min):
                        Min = value
                    if(Min < beta):
                        beta = Min
                    if(beta <= alpha):
                        break;
                return Min;
            
    def get_action(self, node : Node, depth : int, isMax : bool) -> GameAction: # akan menghasilkan pergerakan yang best, sesuai dengan algoritma minimax keluarannya berupa tuple posisi
        pass
    
    def utilitidValue(self, state : GameState) -> int:
        return 0