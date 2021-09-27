#!/usr/bin/env python3

import random

import numpy as np
import pyglet as pg


def measure(column: int):
    """Checks if there need to be taken any measurements and takes them.
    :column: column in which to start measurement
    """
    board_shifted = np.append(board.T[column:], board.T[:column]).reshape(width, height)
    for col_nr, col in enumerate(board_shifted):
        col_nr = (col_nr + column) % width
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
        elif quantum_pos == 0 and col[1] == col[0]:
            measure_column(col_nr, 0)


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
        board[0, column] = draw_counter
        if not second_quantum_move:
            quantum_list.append(draw_counter)
    return a


def create_piece(column) -> bool:
    """Classical piece is created, gets 1 column as input, updates the board after the move and returns a = True
    if the move is possible, otherwise the player has to select another column
    :column: column to place the classical piece in
    :returns: whether the move was possible
    """
    a = check_move(column)
    if a:
        board[0, column] = draw_counter
    return a


def gravity_column(column: int):
    """Puts gravity to the board.
    :column: the column to let gravity act on
    """
    a = board[:, column]
    a = a[a != 0]
    while len(a) <= height - 1:
        a = np.append(np.array([0]), a)
    board[:, column] = a


def check_win() -> int:
    """Checks whether the game is over
    :returns: int>0: player who won, -2: tie, -1: nobody has won yet
    """
    winner = -2
    winturn = (
            2 * width * height
    )  # a number sufficiently big, that the real winturn is smaller for sure
    tempwinturn = -1
    player = -1
    counter = 0

    # check rows
    for row in range(height):
        for column in range(width):
            field = board[row][column]

            winner, winturn, tempwinturn, player, counter = check_field(
                winner, winturn, tempwinturn, player, counter, field
            )
        counter = 0
        tempwinturn = -1

    # check columns
    for column in range(width):
        for row in range(height):
            field = board[row][column]

            winner, winturn, tempwinturn, player, counter = check_field(
                winner, winturn, tempwinturn, player, counter, field
            )
        counter = 0
        tempwinturn = -1

    # check diagonals top to bottom
    for column in range(0, width - psi):
        x = 0
        while (column + x) < width and x < height:
            field = board[x][column + x]
            winner, winturn, tempwinturn, player, counter = check_field(
                winner, winturn, tempwinturn, player, counter, field
            )
            x += 1

        counter = 0
        tempwinturn = -1

    for row in range(1, height - psi):
        x = 0
        while (row + x) < height and x < width:
            field = board[row + x][x]
            winner, winturn, tempwinturn, player, counter = check_field(
                winner, winturn, tempwinturn, player, counter, field
            )
            x += 1

        counter = 0
        tempwinturn = -1

    # check diagonals bottom to top
    for column in range(0, width - psi):
        x = 0
        while (column + x) < width and x < height:
            field = board[height - 1 - x][column + x]
            winner, winturn, tempwinturn, player, counter = check_field(
                winner, winturn, tempwinturn, player, counter, field
            )
            x += 1

        counter = 0
        tempwinturn = -1

    for row in range(1, height - psi):
        x = 0
        while (row + x) < height and x < width:
            field = board[height - 1 - x - row][x]
            winner, winturn, tempwinturn, player, counter = check_field(
                winner, winturn, tempwinturn, player, counter, field
            )
            x += 1

        counter = 0
        tempwinturn = -1

    if 0 not in board and winner == -2:
        return -2

    return winner + 1


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
        new_player = field % player_nr
        if player == new_player:
            counter += 1
            if field > tempwinturn:
                tempwinturn = field

            if counter == psi and tempwinturn < winturn:  # If we have a new winner
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


def get_playercolor(turn: int) -> tuple[int, int, int]:
    """
    :turn: turn of the game
    :returns: color of the player
    """
    if turn == 0:
        color = (190, 190, 190)
    elif turn % player_nr == 0:
        color = (255, 0, 0)
    elif turn % player_nr == 1:
        color = (0, 255, 0)
    elif turn % player_nr == 2:
        color = (0, 0, 255)
    elif turn % player_nr == 3:
        color = (255, 255, 0)
    else:
        color = (100, 100, 100)
    return color


def draw_board():
    """Draws all of the pieces and their labels as well as the arrow.
    """
    circles = []
    labels = []
    for i in range(height):
        for j in range(width):
            c = get_playercolor(board[i, j])
            circle = pg.shapes.Circle(j * (rectangle.width // width) + rectangle.width // (width * 2) + offset_x,
                                      (height - i - 1) * (rectangle.height // height) + rectangle.height // (
                                              height * 2) + offset_y,
                                      rectangle.width // scaling_circ, color=c, batch=batch)
            if board[i, j] in quantum_list:
                circle.opacity = 80
            if board[i, j] != 0:
                label = pg.text.Label(str(board[i, j]), font_size=16, bold=True, color=(25, 25, 25, 255),
                                      x=j * (rectangle.width // width) + rectangle.width // (width * 2) + offset_x,
                                      y=(height - i - 1) * (rectangle.height // height) + rectangle.height // (
                                              height * 2) + offset_y,
                                      anchor_x='center', anchor_y='center')
                labels.append(label)
            circles.append(circle)
    text_turn = pg.text.Label('Turn: ' + str(draw_counter), font_size=int(1.8 * scaling_circ), bold=True,
                              x=int(size_x - 6 * offset_x), y=int(rectangle.height + 5 * offset_y), anchor_x='center',
                              anchor_y='center')
    text_turn.draw()
    batch.draw()
    for elem in labels:
        elem.draw()
    sprite.position = (
        (position + 1) * (rectangle.width // width) + rectangle.width // (width * 2) + offset_x - arrow.width / 2,
        (height - 0.4) * (rectangle.height // height) + rectangle.height // (height * 2) + offset_y)
    sprite.draw()

def draw_win(winner: int):
    """
    :param winner: Player who has won the game
    """
    if winner == -2:
        tie_message = pg.text.Label('Tie!', font_size=int(2 * scaling_circ), bold=True, color=(0, 0, 0, 0),
                                    x=size_x // 2, y=size_y // 2, anchor_x='center',
                                    anchor_y='center')
        tie_message.draw()
    else:
        win_message = pg.text.Label('Player ' + str(winner) + ' has won!', font_size=int(2 * scaling_circ), bold=True, color=(0, 0, 0, 0),
                                  x=size_x//2, y=size_y//2, anchor_x='center',
                                  anchor_y='center')
        win_message.draw()



width, height = 7, 6
player_nr = 2
psi = 4  # number of connected pieces to win
won = -1
draw_counter = 1
board = np.zeros((height, width), dtype="int16")
quantum_list = []
is_quantum_move, second_quantum_move = False, False

global_scaling = width * 15
size_x = int(width * global_scaling)  # 1280
size_y = int(size_x * height / width)  # 720
scaling = 2
scaling_circ = 20
offset_x = size_x // 30  # 10
offset_y = size_y // 30  # 10
position = 0

window = pg.window.Window(size_x, size_y + 120)
batch = pg.graphics.Batch()
rectangle = pg.shapes.Rectangle(offset_x, offset_y, width=int(size_x - 2 * offset_x),
                                height=int((size_x - 2 * offset_x) * height / width), color=(230, 230, 230),
                                batch=batch)
arrow = pg.image.load('arrow.png')
sprite = pg.sprite.Sprite(img=arrow)
sprite.scale = 0.2
draw_board()


@window.event
def on_key_press(symbol, modifiers):
    global board, quantum_list, position, is_quantum_move, second_quantum_move, draw_counter, won
    won = check_win()
    if won == -1:
        if second_quantum_move:
            if symbol == pg.window.key.LEFT:
                position = (position - 1) % width
                arrow.x = position * (rectangle.width // width) + rectangle.width // (width * 2) + offset_x
            elif symbol == pg.window.key.RIGHT:
                position = (position + 1) % width
                arrow.x = position * (rectangle.width // width) + rectangle.width // (width * 2) + offset_x
            elif symbol == pg.window.key.ENTER and create_quantum_piece(position):
                second_quantum_move = False
                draw_counter += 1
                gravity_column(position)
                measure(position)
                for col in range(width):
                    gravity_column(col)
        else:
            if symbol == pg.window.key.Q:
                is_quantum_move = not is_quantum_move
            elif symbol == pg.window.key.LEFT:
                position = (position - 1) % width
                arrow.x = position * (rectangle.width // width) + rectangle.width // (width * 2) + offset_x
            elif symbol == pg.window.key.RIGHT:
                position = (position + 1) % width
                arrow.x = position * (rectangle.width // width) + rectangle.width // (width * 2) + offset_x
            elif symbol == pg.window.key.ENTER:
                if is_quantum_move and create_quantum_piece(position):
                    gravity_column(position)
                    second_quantum_move = True
                elif create_piece(position):
                    draw_counter += 1
                    measure(position)
                    for col in range(width):
                        gravity_column(col)
    else:
        if symbol == pg.window.key.ENTER:
            won = -1
            draw_counter = 1
            board = np.zeros((height, width), dtype="int16")
            quantum_list = []
            is_quantum_move, second_quantum_move = False, False


@window.event
def on_draw():
    global won
    window.clear()
    draw_board()
    if won != -1:
        draw_win(won)


pg.app.run()
