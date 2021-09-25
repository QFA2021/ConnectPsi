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
    for column in board.T:
        quantum_pos = -1  # position of highest quantum piece
        classical_pos = -1  # position of highest classical piece
        for pos, val in enumerate(column):
            if val != 0:
                if val in quantum_list:
                    quantum_pos = pos
                else:
                    classical_pos = pos
        if quantum_pos != -1 and classical_pos != -1 and classical_pos > quantum_pos:
            return_list.append(column)
    return return_list


def measure(column: int):
    """Measures the given column, collapsing quantum super positions.
    :column: the column to measure
    """
    to_measure = board[:, column]
    for pos, val in to_measure:
        if val in quantum_list:
            (piece1, piece2) = np.where(board == val)
            rand = bool(random.getrandbits(1))
            if rand:
                board[piece1] = val
                board[piece2] = 0
            else:
                board[piece2] = val
                board[piece1] = 0
            quantum_list.remove(val)


width, height = 7, 6
player_nr = 2
draw_counter = 0
board = np.zeros((height, width), dtype="int16")
quantum_list = []

if __name__ == main():
    main()
