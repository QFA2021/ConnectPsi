#!/usr/bin/env python3

import random

import numpy as np
import pyglet as pg
from configparser import ConfigParser


def read_config(file: str):
    """Reads a config file and sets the variables.
    :file: path of the file to read
    """
    global WIDTH, HEIGHT, PLAYER_NR, PSI
    conf = ConfigParser()
    conf.read(file)
    if conf['DEFAULT']:
        WIDTH = conf['DEFAULT'].getint('width', 7)
        HEIGHT = conf['DEFAULT'].getint('height', 6)
        PLAYER_NR = conf['DEFAULT'].getint('player_nr', 2)
        PSI = conf['DEFAULT'].getint('psi', 4)
    else:
        print("Config file not found.")


def measure(column: int):
    """Checks if there need to be taken any measurements and takes them.
    :column: column in which to start measurement
    """
    board_shifted = np.append(board.T[column:], board.T[:column], axis=0)
    measure_again = False
    for col_nr_it, col in enumerate(board_shifted):
        col_nr = (col_nr_it + column) % WIDTH
        quantum_pos = -1  # position of highest quantum piece
        classical_pos = -1  # position of highest classical piece
        for pos, val in enumerate(col[::-1]):
            if val != 0:
                if val in quantum_list:
                    quantum_pos = len(col) - 1 - pos
                else:
                    classical_pos = len(col) - 1 - pos
        if quantum_pos != -1 and classical_pos != -1 and classical_pos < quantum_pos:
            measure_column(col_nr, classical_pos)
            measure_again = True
            break
        elif quantum_pos == 0 and col[1] == col[0]:
            measure_column(col_nr, 0)
            measure_again = True
            break
        elif col[0] in quantum_list:
            pieces = np.argwhere(board == col[0])
            if pieces[0, 0] == 0 and pieces[1, 0] == 0:
                measure_column(pieces[0, 1], 0)
                measure_column(pieces[1, 1], 0)
                measure_again = True
                break
    if measure_again:
        measure(column)


def measure_column(column: int, start_point: int):
    """Measures the given column, collapsing quantum super positions.
    :column: the column to measure
    :start_point: row at which the measurement should be started
    """
    to_measure = board[start_point:, column]
    for val in to_measure:
        if val in quantum_list:
            pieces = np.argwhere(board == val)
            rand = random.randint(0, len(pieces) - 1)
            board[pieces[rand, 0], pieces[rand, 1]] = val
            for i in range(len(pieces)):
                if i == rand:
                    continue
                board[pieces[i, 0], pieces[i, 1]] = 0
            quantum_list.remove(val)


def check_move(column: int) -> bool:
    """Checks if a move in a certain column is possible.
    :column: the column to check
    :returns: boolean whether the move is possible
    """
    if board[0, column] == 0:
        return True
    else:
        return False


def create_quantum_piece(column) -> bool:
    """Quantum piece is created, updates the board after the move.
    :column: column to place the quantum piece in
    :returns: whether the move was possible
    """
    a = check_move(column)
    if a:
        board[0, column] = turn_counter
        if not second_quantum_move:
            quantum_list.append(turn_counter)
    return a


def create_piece(column) -> bool:
    """Classical piece is created, gets 1 column as input, updates the board after the move and returns a = True
    if the move is possible, otherwise the player has to select another column
    :column: column to place the classical piece in
    :returns: whether the move was possible
    """
    a = check_move(column)
    if a:
        board[0, column] = turn_counter
    return a


def gravity_column(column: int):
    """Puts gravity to the board.
    :column: the column to let gravity act on
    """
    a = board[:, column]
    a = a[a != 0]
    while len(a) <= HEIGHT - 1:
        a = np.append(np.array([0]), a)
    board[:, column] = a


def check_win() -> int:
    """Checks whether the game is over
    :returns: int>0: player who won, -2: tie, -1: nobody has won yet
    """
    winner = -1
    winturn = (
            2 * WIDTH * HEIGHT
    )  # a number sufficiently big, that the real winturn is smaller for sure
    tempwinturn = -1
    player = -1
    counter = 0

    # check rows
    for row in range(HEIGHT):
        for column in range(WIDTH):
            field = board[row][column]

            winner, winturn, tempwinturn, player, counter = check_field(
                winner, winturn, tempwinturn, player, counter, field
            )
        counter = 0
        tempwinturn = -1

    # check columns
    for column in range(WIDTH):
        for row in range(HEIGHT):
            field = board[row][column]

            winner, winturn, tempwinturn, player, counter = check_field(
                winner, winturn, tempwinturn, player, counter, field
            )
        counter = 0
        tempwinturn = -1

    # check diagonals top to bottom
    for column in range(0, WIDTH - PSI + 2):
        x = 0
        while (column + x) < WIDTH and x < HEIGHT:
            field = board[x][column + x]
            winner, winturn, tempwinturn, player, counter = check_field(
                winner, winturn, tempwinturn, player, counter, field
            )
            x += 1

        counter = 0
        tempwinturn = -1

    for row in range(1, HEIGHT - PSI + 2):
        x = 0
        while (row + x) < HEIGHT and x < WIDTH:
            field = board[row + x][x]
            winner, winturn, tempwinturn, player, counter = check_field(
                winner, winturn, tempwinturn, player, counter, field
            )
            x += 1

        counter = 0
        tempwinturn = -1

    # check diagonals bottom to top
    for column in range(0, WIDTH - PSI + 2):
        x = 0
        while (column + x) < WIDTH and x < HEIGHT:
            field = board[HEIGHT - 1 - x][column + x]
            winner, winturn, tempwinturn, player, counter = check_field(
                winner, winturn, tempwinturn, player, counter, field
            )
            x += 1

        counter = 0
        tempwinturn = -1

    for row in range(1, HEIGHT - PSI + 2):
        x = 0
        while (row + x) < HEIGHT and x < WIDTH:
            field = board[HEIGHT - x - row][x]
            winner, winturn, tempwinturn, player, counter = check_field(
                winner, winturn, tempwinturn, player, counter, field
            )
            x += 1

        counter = 0
        tempwinturn = -1

    if 0 not in board and winner == -2:
        return -2

    return winner if winner != 0 else PLAYER_NR


def check_field(
        winner: int, winturn: int, tempwinturn: int, player: int, counter: int, field: int
) -> tuple[int, int, int, int, int]:
    """Checks field for relevant changes for the check_win method.
    :winner: current winner
    :winturn: current minimal number of turns to win
    :tempwinturn: temporary winturn number
    :player: owner of the previously checked piece
    :counter: counts the connected pieces
    :field: current place on the board
    :returns: new winner, winturn, tempwinturn, player and counter
    """
    if field != 0 and field not in quantum_list:  # If  a classical piece lies there
        new_player = field % PLAYER_NR
        if player == new_player:
            counter += 1
            if field > tempwinturn:
                tempwinturn = field

            if counter == PSI and tempwinturn < winturn:  # If we have a new winner
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

    return winner, winturn, tempwinturn, player, counter


def get_playercolor(d):
    if d == 0:
        a = (190, 190, 190)
    elif d % PLAYER_NR == 0:
        a = (255, 0, 0)
    elif d % PLAYER_NR == 1:
        a = (0, 255, 0)
    elif d % PLAYER_NR == 2:
        a = (0, 0, 255)
    elif d % PLAYER_NR == 3:
        a = (255, 255, 0)
    elif d % PLAYER_NR == 4:
        a = (0, 255, 255)
    elif d % PLAYER_NR == 5:
        a = (255, 0, 255)
    else:
        a = (100, 100, 100)
    return a


def draw_board():
    """Draws all of the pieces and their labels as well as the arrow.
    """
    circles = []
    labels = []

    for i in range(HEIGHT):
        for j in range(WIDTH):
            c = get_playercolor(board[i, j])
            circle = pg.shapes.Circle(OFFSET_X + (CIRC_DIST + R) * (2 * j + 1),
                                      2 * (HEIGHT - i) * (CIRC_DIST + R) - R + CIRC_DIST,
                                      R, color=c, batch=batch)
            if board[i, j] in quantum_list:
                circle.opacity = 80
            if board[i, j] != 0:
                label = pg.text.Label(str(board[i, j]), font_size=int(0.4 * R), bold=True, color=(25, 25, 25, 255),
                                      x=OFFSET_X + (CIRC_DIST + R) * (2 * j + 1),
                                      y=2 * (HEIGHT - i) * (CIRC_DIST + R) - R + CIRC_DIST,
                                      anchor_x='center', anchor_y='center')
                labels.append(label)
            circles.append(circle)
    text_turn = pg.text.Label('Turn: ' + str(turn_counter), font_size=50, bold=True,
                              x=int(SIZE_X - 6 * OFFSET_X - 50), y=int(rectangle.height + 7 * OFFSET_Y),
                              anchor_x='center',
                              anchor_y='center')
    text_turn.draw()

    if is_quantum_move:
        label_qm = pg.text.Label('Q', font_size=50, bold=True, italic=True, x=3 * OFFSET_X,
                                 y=int(rectangle.height + 7 * OFFSET_Y),
                                 anchor_x='center', anchor_y='center')
        label_qm.draw()
    batch.draw()
    for elem in labels:
        elem.draw()
    sprite.position = (
        position * 2 * (CIRC_DIST + R) + CIRC_DIST + OFFSET_X + R - 0.5 * sprite.width,
        (SIZE_Y - 140))
    sprite.draw()


def draw_win(winner: int):
    """Draws the text for the winner of the game.
    :param winner: Player who has won the game
    """
    if winner == -2:
        tie_message = pg.text.Label('Tie!', font_size=40, bold=True, color=(0, 0, 0, 255),
                                    x=SIZE_X // 2, y=SIZE_Y // 2, anchor_x='center',
                                    anchor_y='center')
        tie_message.draw()
    else:
        win_message = pg.text.Label('Player ' + str(winner) + ' has won!', font_size=40, bold=True,
                                    color=(0, 0, 0, 255),
                                    x=SIZE_X // 2, y=SIZE_Y // 2, anchor_x='center',
                                    anchor_y='center')
        win_message.draw()


WIDTH = 7  # width of the board
HEIGHT = 6  # height of the board
PLAYER_NR = 2  # number of players
PSI = 4  # number of connected pieces to win
read_config("connectpsi.conf")

# Backend variables
won = -1  # player who has won
turn_counter = 1
board = np.zeros((HEIGHT, WIDTH), dtype="int16")
quantum_list = []  # list of quantum pieces
is_quantum_move, second_quantum_move = False, False

TOP_DISTANCE = 160  # distance from the field to the top of the window
SIZE_X = int(1280 * 0.5)  # x size of the window
SIZE_Y = int(SIZE_X * HEIGHT / WIDTH) + TOP_DISTANCE  # y size of the window
OFFSET_X = 20  # x margin of the field
OFFSET_Y = 20  # y margin of the field
CIRC_DIST = 8  # distance between two circles
R = (SIZE_X - 2 * OFFSET_X) / (2 * WIDTH) - CIRC_DIST  # radius of the circles
position = 0  # column of a piece

window = pg.window.Window(SIZE_X, SIZE_Y)
batch = pg.graphics.Batch()
rectangle = pg.shapes.Rectangle(OFFSET_X, OFFSET_Y, width=int(SIZE_X - 2 * OFFSET_X),
                                height=int((SIZE_X - 2 * OFFSET_X) * HEIGHT / WIDTH), color=(230, 230, 230),
                                batch=batch)
arrow = pg.image.load('arrow.png')
sprite = pg.sprite.Sprite(img=arrow)
sprite.scale = 0.2

draw_board()


@window.event
def on_key_press(symbol, modifiers):
    global board, quantum_list, position, is_quantum_move, second_quantum_move, turn_counter, won
    if won != -1:
        if symbol == pg.window.key.ENTER:
            won = -1
            turn_counter = 1
            board = np.zeros((HEIGHT, WIDTH), dtype="int16")
            quantum_list = []
            is_quantum_move, second_quantum_move = False, False
    else:
        if second_quantum_move:
            if symbol == pg.window.key.LEFT:
                position = (position - 1) % WIDTH
                arrow.x = position * (rectangle.width // WIDTH) + rectangle.width // (WIDTH * 2) + OFFSET_X
            elif symbol == pg.window.key.RIGHT:
                position = (position + 1) % WIDTH
                arrow.x = position * (rectangle.width // WIDTH) + rectangle.width // (WIDTH * 2) + OFFSET_X
            elif symbol == pg.window.key.ENTER and create_quantum_piece(position):
                second_quantum_move = False
                turn_counter += 1
                gravity_column(position)
                measure(position)
                for col in range(WIDTH):
                    gravity_column(col)
        else:
            if symbol == pg.window.key.Q:
                is_quantum_move = not is_quantum_move
            elif symbol == pg.window.key.LEFT:
                position = (position - 1) % WIDTH
                arrow.x = position * (rectangle.width // WIDTH) + rectangle.width // (WIDTH * 2) + OFFSET_X
            elif symbol == pg.window.key.RIGHT:
                position = (position + 1) % WIDTH
                arrow.x = position * (rectangle.width // WIDTH) + rectangle.width // (WIDTH * 2) + OFFSET_X
            elif symbol == pg.window.key.ENTER:
                if is_quantum_move and create_quantum_piece(position):
                    gravity_column(position)
                    second_quantum_move = True
                elif create_piece(position):
                    turn_counter += 1
                    measure(position)
                    for col in range(WIDTH):
                        gravity_column(col)
        won = check_win()
        if won != -1:
            draw_win(won)


@window.event
def on_draw():
    global won
    window.clear()
    draw_board()
    if won != -1:
        draw_win(won)


pg.app.run()
