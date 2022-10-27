from collections import namedtuple
import connectfour

GameState = namedtuple('GameState', ['board', 'turn'])

def board_size() -> int:
    '''Takes user input for size of a connect four board and determines if it is valid
    Return - valid column and row inputs'''
    try:
        columnInput = int(input('How many columns do you want to play with? (4-20) '))
        rowInput = int(input('How many rows do you want to play with? (4-20) '))
        return columnInput, rowInput
    except ValueError:
        print('Column and row must be valid numbers. ')
        return 0, 0

def board_input() -> str:
    '''Takes user input for a move and determines if it is valid
    Return - valid connect four move inputs'''
    dropOrPop = input('Do you want to drop or pop a piece? ')
    try:
        turnInput = int(input('Choose a column '))
    except ValueError:
        print('Column must be a number.')
    return dropOrPop, turnInput

def find_winner(winner: int | str) -> str:
    '''Finds the winner of the connect four game based on connectfour.py and ICS server output
    Parameters - output from connectfour.py and ICS server output
    Return - string printing out the color of the winner'''
    if winner == 2 or winner == 'WINNER_RED':
        return 'RED is the winner!'
    elif winner == 1 or winner == 'WINNER_YELLOW':
        return 'YELLOW is the winner!'

def whos_turn(num: int) -> str:
    '''Identifies if it is red or yellow's turn (based on connectfour.py's variables)
    Parameters - finds the turn based on connectfour.py 
    return - string of whose turn it is'''
    if num == 1:
        return 'RED'
    elif num == 2:
        return 'YELLOW'

def print_board(game_state: GameState) -> None:
    '''Prints out the board of a connect four game
    Parameter - connectfour game
    Return - none, prints out the board of the connect four game'''
    numOfColumns = connectfour.columns(game_state)
    numOfRows = connectfour.rows(game_state)
    formatBoard = format('{block:^2}')
    board, turn = game_state
    for numbers in range(1, len(board) + 1):
        print(formatBoard.format(block = numbers), end = ' ')
    print()
    for row in range(0, numOfRows):
        for column in range(0, numOfColumns):
            if board[column][row] == 0:
                print(formatBoard.format(block = '.'), end = ' ')
            else:
                if (board[column][row] == 1):
                    print(formatBoard.format(block = 'R'), end = ' ')
                elif (board[column][row] == 2):
                    print(formatBoard.format(block = 'Y'), end = ' ')
        print()
