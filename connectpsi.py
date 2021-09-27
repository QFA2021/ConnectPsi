#!/usr/bin/env python3

import random

import numpy as np
import pyglet as pg


def check_measure() -> list[tuple[int, int]]:
    """Checks if there need to be taken any measurements.
    :returns: columns to be measured and point to start measurement
    """
    return_list = []  # list of columns to be measured
    for col_nr, column in enumerate(board.T):
        quantum_pos = -1  # position of highest quantum piece
        classical_pos = 100000  # position of highest classical piece
        for pos, val in enumerate(column[::-1]):
            if val != 0:
                if val in quantum_list:
                    quantum_pos = len(column) - 1 - pos
                else:
                    classical_pos = len(column) - 1 - pos
        if (quantum_pos != -1 and classical_pos != -1 and classical_pos < quantum_pos) or quantum_pos == 0:
            return_list.append((col_nr, classical_pos))
    return return_list


def measure(column: int, start_point: int):
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
    else:
        print("select another column")  # TODO: game logic
    return a


def create_piece(column) -> bool:
    """Classical piece is created, gets 1 column as input, updates the board after the move and returns a = True if the move is possible, otherwise the player has to select another column
    :column: column to place the classical piece in
    :returns: whether the move was possible
    """
    a = check_move(column)
    if a:
        board[0, column] = draw_counter
    else:
        print("select another column")  # TODO: game logic
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
    :returns: int>0: player who won, -2: tie, -1: nobody has won, yet
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

    if not 0 in board and winner == -2:
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


def get_playercolor(d):
    if d == 0:
        a = (190, 190, 190)
    elif d % player_nr == 0:
        a = (255, 0, 0)
    elif d % player_nr == 1:
        a = (0, 255, 0)
    elif d % player_nr == 2:
        a = (0, 0, 255)
    elif d % player_nr == 3:
        a = (255, 255, 0)
    elif d % player_nr == 4:
        a = (0,255, 255)
        
    return (a)






def draw_board():
    liste = []
    labels = []
      
    for i in range(height):
        for j in range(width):
            c = get_playercolor(board[i, j])
            circle = pg.shapes.Circle(offset_x + (const2 + r)*(2*j+1),
                                      2*(height - i) * (const2 + r) - r + const2,
                                      r, color=c, batch=batch)
            if board[i, j] in quantum_list:
                circle.opacity = 80
            if board[i, j] != 0:
                label = pg.text.Label(str(board[i, j]), font_size=int(0.4*r), bold=True, color=(25, 25, 25, 255),
                                      x=offset_x + (const2 + r) * (2 * j + 1),
                                      y=2 * (height - i) * (const2 + r) - r + const2,
                                      anchor_x='center', anchor_y='center')
                labels.append(label)
            liste.append(circle)
    text_turn = pg.text.Label('Turn: ' + str(draw_counter), font_size=50, bold=True,
                              x=int(size_x - 6 * offset_x - 100), y=int(size_y-40), anchor_x='center',
                              anchor_y='center')
    text_turn.draw()

    if is_quantum_move:
        label_qm = pg.text.Label('Q', font_size=50, bold = True, italic = True, x = 2.9*offset_x,
                                 y=int(rectangle.height + 5 * offset_y), 
                        anchor_x='center', anchor_y='center' )
        label_qm.draw()
    batch.draw()
    for elem in labels:
        elem.draw()
    sprite.position = (
        (pos) * 2*(const2 + r) + const2 + offset_x + r - 0.5*sprite.width,
        (size_y - 140))
    sprite.draw()


width, height = 7, 6
player_nr = 2
draw_counter = 1
board = np.zeros((height, width), dtype="int16")
quantum_list = []
psi = 4  # number of connected pieces to win
is_quantum_move, second_quantum_move = False, False


#global_scaling = width * 15
TOP_DISTANCE = 160
size_x = 1280
size_y = int(size_x * height / width) + TOP_DISTANCE
#scaling = 2
#scaling_circ = 20
offset_x = 20
offset_y = 20
const2 = 8
r = (size_x-2*offset_x)/(2*width) - const2
pos = 0

window = pg.window.Window(size_x, size_y)
batch = pg.graphics.Batch()
rectangle = pg.shapes.Rectangle(offset_x, offset_y, width=int(size_x - 2 * offset_x),
                                height=int((size_x - 2 * offset_x) * height / width), color=(230, 230, 230),
                                batch=batch)
arrow = pg.image.load('arrow2.png')
sprite = pg.sprite.Sprite(img=arrow)
sprite.scale = 0.2
draw_board()


@window.event
def on_key_press(symbol, modifiers):
    global pos, is_quantum_move, second_quantum_move, draw_counter
    if second_quantum_move:
        if symbol == pg.window.key.LEFT:
            pos = (pos - 1) % (width)
            arrow.x = pos * (rectangle.width // width) + rectangle.width // (width * 2) + offset_x
        elif symbol == pg.window.key.RIGHT:
            pos = (pos + 1) % (width)
            arrow.x = pos * (rectangle.width // width) + rectangle.width // (width * 2) + offset_x
        elif symbol == pg.window.key.ENTER:
            create_quantum_piece(pos)
            second_quantum_move = False
            draw_counter += 1
            for col, start_point in check_measure():
                measure(col, start_point)
            for col in range(width):
                gravity_column(col)
    else:
        if symbol == pg.window.key.Q:
            is_quantum_move = not is_quantum_move
        elif symbol == pg.window.key.LEFT:
            pos = (pos - 1) % (width)
            arrow.x = pos * (rectangle.width // width) + rectangle.width // (width * 2) + offset_x
        elif symbol == pg.window.key.RIGHT:
            pos = (pos + 1) % (width)
            arrow.x = pos * (rectangle.width // width) + rectangle.width // (width * 2) + offset_x
        elif symbol == pg.window.key.ENTER:
            if is_quantum_move:
                create_quantum_piece(pos)
                gravity_column(pos)
                second_quantum_move = True
            else:
                create_piece(pos)
                draw_counter += 1
                for col, start_point in check_measure():
                    measure(col, start_point)
                for col in range(width):
                    gravity_column(col)


@window.event
def on_draw():
    window.clear()
    draw_board()


pg.app.run()
