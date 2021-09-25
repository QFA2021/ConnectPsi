#!/usr/bin/env python3

import numpy as np
import pyglet as pg
import random


def main():
    """Main method to be run when executing file.
    board: array functioning as the game board
    quantum_list: list of quantum stones
    """
    pass


def check_measure() -> array[int]:
    """Checks if there need to be taken any measurements.
    :returns: columns to be measured
    """
    return_list = []  # list of columns to be measured
    for col_nr, column in enumerate(board.T):
        quantum_pos = -1  # position of highest quantum piece
        classical_pos = -1  # position of highest classical piece
        for pos, val in enumerate(column[::-1]):
            if val != 0:
                if val in quantum_list:
                    quantum_pos = pos - 1 - pos
                else:
                    classical_pos = pos - 1 - pos
        if quantum_pos != -1 and classical_pos != -1 and classical_pos < quantum_pos:
            return_list.append(col_nr)
    return return_list


def measure(column: int, start_point: int):
    """Measures the given column, collapsing quantum super positions.
    :column: the column to measure
    :start_point: row at which the measurement should be started
    """
    to_measure = board[start_point:, column]
    for pos, val in enumerate(to_measure):
        if val in quantum_list:
            (piece1, piece2) = np.argwhere(board == val)
            rand = bool(random.getrandbits(1))
            if rand:
                board[piece1[0], piece1[1]] = val
                board[piece2[0], piece2[1]] = 0
            else:
                board[piece1[0], piece1[1]] = 0
                board[piece2[0], piece2[1]] = val
            quantum_list.remove(val)
            
            
def check_move(column):
    
    """
    returns True is there is enough space in the column to put a piece here
    """
    
    if board[0, column] == 0:
        return True
    else :
        return False
 
    
 
def create_quantum_piece(column1, column2):
    
    """
    quantum piece is created, gets 2 columns as input, updates the board after the 
    move and returns a, b = True, True if the move is possible, otherwise the player
    has to select another column
    """
    
    a = check_move(column1)
    if a == True:
        board[0, column1] = draw_counter
        gravity_column(column1)
    else :
        print("select another column")
    b = check_move(column2)
    if b == True:
        board[0, column2] = draw_counter
        gravity_column(column2)
    else :
        print("select another column")
    if a == True and b == True:
        quantum_list = quantum_list + [draw_counter]
    return(a, b)



def gravity_column(column):
    
    """
    puts gravity to the board
    """
    
    a = board[:, column]
    a = a[a != 0]
    while len(a) <= height-1:
        a = np.append(np.array([0]), a)
        if len(a) == height:
            break
    board[:, column] = a


    
def create_piece(column):
    
    """
    classical piece is created, gets 1 column as input, updates the board after the 
    move and returns a = True if the move is possible, otherwise the player
    has to select another column
    """
    
    a = check_move(column)
    if a == True:
        board[0, column] = draw_counter
        gravity_column(column)
    else :
        print("select another column")



width, height = 7, 6
player_nr = 2
draw_counter = 0
board = np.zeros((height, width), dtype="int16")
quantum_list = []

if __name__ == main():
    main()
