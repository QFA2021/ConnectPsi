#!/usr/bin/env python3

import numpy as np
import pyglet as pg


def main():
    """
    Main method to be run when executing file.
    board: array functioning as the game board
    quantum_list: list of quantum stones
    """
    pass


width, height = 7, 6
player_nr = 2
draw_counter = 0
board = np.zeros((height, width))
quantum_list = []
psi = 4                            #number of connected pieces to win

if __name__ == main():
    main()


def check_win() -> int:
    winner = -1
    winturn = 2 * width * height  # a number sufficiently big, that the real winturn is smaller for sure
    tempwinturn = -1
    player = -1
    counter = 0
    # check rows
    for row in range(height):
        for column in range(width):
            field = board[row][column]

            if (field != 0 and field not in quantum_list):         # If  a classical piece lies there
                new_player = field % player_nr
                if (player == new_player):
                    counter += 1
                    if (field > tempwinturn):
                        tempwinturn = field

                    if (counter == psi and tempwinturn < winturn):  # If we have a new winner
                        winturn = tempwinturn
                        winner = player

                else:
                    player = new_player
                    counter = 1
                    tempwinturn = field
            else:
                counter = 0
                player = -1
                tempwinturn = -1

            counter = 0
            tempwinturn = -1

    # check columns
    for column in range(width):
        for row in range(height):

            field = board[row][column]

            if (field != 0 and field not in quantum_list):  # If  a classical piece lies there
                new_player = field % player_nr
                if (player == new_player):
                    counter += 1
                    if (field > tempwinturn):
                        tempwinturn = field

                    if (counter == psi and tempwinturn < winturn):  # if we have a new winner
                        winturn = tempwinturn
                        winner = player

                else:
                    player = new_player
                    counter = 1
                    tempwinturn = field
            else:
                counter = 0
                player = -1
                tempwinturn = -1

            counter = 0
            tempwinturn = -1

    return -1
