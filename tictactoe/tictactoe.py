"""
Tic Tac Toe Player
"""

import math
import copy
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    global turn
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    turn_counter = 0
    for row in (range (3)):
        for column in (range (3)):
            if board[row][column] != EMPTY:
                turn_counter +=1
    if turn_counter % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for x in range (3):
        for y in range(3):
            if board[x][y] == None:
                possible_moves.add((x,y))
    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    copied_board = copy.deepcopy(board)
    copied_board[action[0]][action[1]] = player(board) 
    return copied_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[0][1] and board[0][1] == board[0][2]:
        return board[0][0]
    elif board[1][0] == board[1][1] and board[1][1] == board[1][2]:
        return board[1][0]
    elif board[2][0] == board[2][1] and board[2][1] == board[2][2]:
        return board[2][0]
    elif board[0][0] == board[1][0] and board[1][0] == board[2][0]:
        return board[0][0]
    elif board[0][1] == board[1][1] and board[1][1] == board[2][1]:
        return board[0][1]
    elif board[0][2] == board[1][2] and board[1][2] == board[2][2]:
        return board[0][2]
    elif board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    elif board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return (True)
    else:
        for row in board:
            for cell in row:
                if cell is None:
                    return (False)
                else:
                    continue
        return (True)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    condition = winner(board)
    if condition == X:
        return 1
    elif condition == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        if player(board) == X:
            value, move = max_board(board)
            return move
        else:
            value, move = min_board(board)
            return move

def max_board(board):
    if terminal(board):
        return utility(board),None
    max = float('-inf')
    move = None
    for action in actions(board):
        min, res = min_board(result(board,action))
        if min > max:
            max = min
            move = action
            if max == 1:
                return max, move
    return max, move
            
def min_board(board):
    if terminal(board):
            return utility(board),None
    min = float('inf')
    move = None
    for action in actions(board):
        max, res = max_board(result(board,action))
        if max < min:
            min = max
            move = action
            if min == -1:
                return min, move
    return min, move

                
                    
                


