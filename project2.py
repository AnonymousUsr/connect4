from collections import namedtuple
import connectfour

GameState = namedtuple('GameState', ['board', 'turn'])

def start_game() -> GameState:
    newGame = None
    userInput = input('Do you want to play a game of Connect Four? ')
    if userInput.lower() == 'yes':
        columnInput = int(input('How many columns do you want to play with? (4-20) '))
        rowInput = int(input('How many rows do you want to play with? (4-20) '))
        if (4 <= columnInput <= 20) and (4 <= rowInput <= 20):
            newGame = connectfour.new_game(columnInput, rowInput)
        else:
            print('Invalid values. Try again.')
            start_game()
    elif userInput.lower() == 'no':
        print('Okay')
        newGame = None
    else:
        print('Enter in yes or no')
        start_game()
    return newGame

def take_turn(game_state: GameState) -> GameState:
    newGameState = None
    print_board(game_state)
    dropOrPop = input('Do you want to drop or pop a piece? ')
    turnInput = int(input('Choose a column '))
    try:
        if dropOrPop.lower() == 'drop':
            newGameState = connectfour.drop(game_state, turnInput-1)
        elif dropOrPop.lower() == 'pop':
            newGameState = connectfour.pop(game_state, turnInput-1)
        else:
            print(connectfour.InvalidMoveError)
    except connectfour.InvalidMoveError or connectfour.GameOverError:
        print('Try a different move')
    return newGameState

def until_winner(game_state: GameState):
    if (game_state != None):
        newGameState = take_turn(game_state)
        while connectfour.winner(newGameState) == 0:
            newGameState = take_turn(newGameState)
    

def print_board(game_state: GameState):
    numOfColumns = connectfour.columns(game_state)
    numOfRows = connectfour.rows(game_state)
    formatBoard = format('{block:^2}')
    board, turn = game_state
    for numbers in range(1, len(board[0]) + 1):
        print(formatBoard.format(block = numbers), end = ' ')
    print()
    for row in board:
        for item in row:
            if item == 0:
                print(formatBoard.format(block = '.'), end = ' ')
            else:
                print(item)
        print()

if __name__ == "__main__":
    startedGame = start_game()
    until_winner(startedGame)