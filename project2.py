from collections import namedtuple
import connectfour

GameState = namedtuple('GameState', ['board', 'turn'])

def start_game() -> GameState:
    newGame = None
    while newGame == None:
        userInput = input('Do you want to play a game of Connect Four? ')
        if userInput.lower() == 'yes':
            columnInput = int(input('How many columns do you want to play with? (4-20) '))
            rowInput = int(input('How many rows do you want to play with? (4-20) '))
            if (4 <= columnInput <= 20) and (4 <= rowInput <= 20):
                newGame = connectfour.new_game(columnInput, rowInput)
                return newGame
            else:
                print('Invalid values. Try again.')
        elif userInput.lower() == 'no':
            print('Okay')
            return None
        else:
            print('Enter in yes or no')

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
        print('Try a different move')
    finally:
        return newGameState

def until_winner(game_state: GameState) -> int:
    if (game_state != None):
        newGameState = take_turn(game_state)
        while connectfour.winner(newGameState) == 0:
            newGameState = take_turn(newGameState)
    else:
        newGameState = take_turn(game_state)
    print_board(newGameState)
    return(newGameState[1])

def whos_turn(num: int) -> str:
    if num == 1:
        return 'RED'
    elif num == 2:
        return 'YELLOW'

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

if __name__ == "__main__":
    startedGame = start_game()
    winner = until_winner(startedGame)
    if winner == 2:
        print('RED is the winner!')
    elif winner == 1:
        print('YELLOW is the winner!')