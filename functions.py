from collections import namedtuple
import connectfour

GameState = namedtuple('GameState', ['board', 'turn'])

#Allows the user to make a valid move
def take_turn(game_state: GameState) -> GameState:
    newGameState = game_state
    print_board(game_state)
    print('It is ' + whos_turn(game_state[1]) + '\'s turn')
    try:
        dropOrPop = input('Do you want to drop or pop a piece? ')
        turnInput = int(input('Choose a column '))
        if dropOrPop.lower() == 'drop':
            newGameState = connectfour.drop(game_state, turnInput-1)
        elif dropOrPop.lower() == 'pop':
            newGameState = connectfour.pop(game_state, turnInput-1)
    except:
        print('InvalidMoveError: Try a different move.')
    finally:
        return newGameState

def something(move: str, col: int):
    newGameState = connectfour.drop(move, col-1)

#Repeats the connect four game until a winner is found and returns the winner
def until_winner(game_state: GameState) -> int:
    if (game_state != None):
        newGameState = take_turn(game_state)
        while connectfour.winner(newGameState) == 0:
            newGameState = take_turn(newGameState)
    else:
        newGameState = take_turn(game_state)
    print_board(newGameState)
    return(newGameState[1])

def find_winner(winner: int) -> str:
    if winner == 2:
        return 'RED is the winner!'
    elif winner == 1:
        return 'YELLOW is the winner!'

#Identifies if it is red or yellow's turn (based on connectfour.py's variables)
def whos_turn(num: int) -> str:
    if num == 1:
        return 'RED'
    elif num == 2:
        return 'YELLOW'

#Prints out the board of a connect four game
def print_board(game_state: GameState) -> None:
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
