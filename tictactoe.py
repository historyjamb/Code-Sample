"""
Tic Tac Toe Player
"""

import math
import copy
from collections import Counter
from random import choice

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # if initial game state, X goes first
    if (board == initial_state()):
        return X

    # elif game over, return None
    elif (terminal(board)):
        return None

    # else return player with fewer moves on board
    else:
        # Flatten list
        total_moves = sum(board, [])

        if (total_moves.count(X) > total_moves.count(O)):
            return O
        else:
            return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # If board in terminal state, return empty set
    if terminal(board):
        return set()

    # Add all EMPTY locations to a set
    possible = set()

    for row in range(0, len(board)):
        for col in range(0, len(board[row])):
            if board[row][col] is EMPTY:
                possible.add((row, col))

    return possible


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i = action[0]
    j = action[1]

    # raise exception if action is not valid
    if board[i][j] is not EMPTY:
        raise ValueError("Action invalid: space already taken")

    elif i not in range(0, len(board)) or j not in range(0, len(board[0])):
        raise ValueError("Action invalid: action does not exist")

    # make copy of original board
    board_copy = copy.deepcopy(board)

    # return the board_copy after making move (i, j)
    board_copy[i][j] = player(board)
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    num_rows = len(board)
    num_cols = len(board[0])    # Note: assumes all rows have the same #columns

    # Check for row winner
    for row in board:
        if row[0] is not EMPTY and all([element == row[0] for element in row]):
            return row[0]

    # Check for col winner
    for col in range(0, num_cols):
        c = board[0][col]   # first element in column c
        if c is not EMPTY:
            if all([board[row][col] == c for row in range(1, num_rows)]):
                return c

    # Check for diagonal win: diagonal through upper left square
    if board[0][0] is not EMPTY:
        if all([board[0][0] == board[r][r] for r in range(1, num_rows)]):
            return board[0][0]

    # Check for diagonal: diagonal win through upper right square s
    s = board[0][len(board[0]) - 1]
    if s is not EMPTY:

        # Check all squares in diagonal have the same value as s
        if all([board[r][num_rows - r - 1] == s for r in range(1, num_rows)]):
            return s

    # if winner not found, return None
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If winner exists, return True
    if winner(board) is not None:
        return True

    # If no winner, return True if no more EMPTY spots
    else:
        # Flatten list
        total_moves = sum(board, [])

        if total_moves.count(EMPTY):
            return False
        else:
            return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Store optimal action(s) in a list
    best_options = []

    # If computer is maximizer (next move is X)
    if player(board) == X:

        # Keeps track of the current best utility score
        max_util_score = -1

        for a in actions(board):
            # Store utility score of action a in a_score
            a_score = min_value(result(board, a))

            # Disregard a if less optimal than actions in best_options
            if a_score < max_util_score:
                continue

            # if better move is found, clear best_options before appending
            elif a_score > max_util_score:
                max_util_score = a_score
                best_options.clear()

            # Append only if a_score >= max_util_score
            best_options.append(a)

    # Computer is minimizer (next move is O)
    else:
        # Keeps track of the current best utility score
        min_util_score = 1

        # Evaluate possible moves
        for a in actions(board):
            # Store utility score of action a in a_score
            a_score = max_value(result(board, a))

            # Disregard a if less optimal than actions in best_options
            if a_score > min_util_score:
                continue

            # if better move is found, clear best_options before appending
            elif a_score < min_util_score:
                best_options.clear()
                min_util_score = a_score

            # Append only if a_score <= min_util_score
            best_options.append(a)

    # return random action from best_options list
    return choice(best_options)


def max_value(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for a in actions(board):
        v = max(v, min_value(result(board, a)))
    return v


def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for a in actions(board):
        v = min(v, max_value(result(board, a)))
    return v
