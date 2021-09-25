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
        if (quantum_pos != -1 and classical_pos != -1 and classical_pos < quantum_pos) or quantum_pos == 0:
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


width, height = 7, 6
player_nr = 2
draw_counter = 0
board = np.zeros((height, width), dtype="int16")
quantum_list = []

if __name__ == main():
    main()
