import socket
from collections import namedtuple
import project2sockets
import functions
import connectfour

GameState = namedtuple('GameState', ['board', 'turn'])

def start_game():
    newGame = None
    while newGame == None:
        columnInput = int(input('How many columns do you want to play with? (>4) '))
        rowInput = int(input('How many rows do you want to play with? (>4) '))
        if (4 <= columnInput) and (4 <= rowInput):
            newGame = connectfour.new_game(columnInput, rowInput)
            return newGame
        else:
            print('Invalid values. Try again.')

def find_space(text: str) -> bool:
    for letter in text.strip():
        if letter == (' ') or letter == ('   '):
            return True
    return False

def until_winner(game_state: GameState) -> int:
    if (game_state != None):
        newGameState = take_turn(game_state)
        while connectfour.winner(newGameState) == 0:
            newGameState = take_turn(newGameState)
    else:
        newGameState = take_turn(game_state)
    functions.print_board(newGameState)
    return(newGameState[1])

def _turn(move: str, col: int, game_state: GameState) -> GameState:
    newGameState = game_state
    print('It is ' + functions.whos_turn(game_state[1]) + '\'s turn')
    try:
        if move.lower() == 'drop':
            newGameState = connectfour.drop(game_state, col-1)
        elif move.lower() == 'pop':
            newGameState = connectfour.pop(game_state, col-1)
    except:
        print('InvalidMoveError: Try a different move.')
    finally:
        return newGameState

if __name__ == '__main__':
    count = 0
    username = (input('Enter a username: ')).strip()
    startedGame = start_game()
    print('YOU ARE RED')
    if not find_space(username):
        while True:
            try:
                move, col, message, message2, message3, count = project2sockets.run_protocol(username, len(startedGame[0]), len(startedGame[0][0]), count)
                if message2 != 'INVALID':
                    startedGame = _turn(move, col, startedGame)
                    functions.print_board(startedGame)
                    splitMessage = message2.split(' ')
                    print('Computer Move: ' + message2)
                    startedGame = _turn(splitMessage[0], int(splitMessage[1]), startedGame)
                elif message == 'WINNER_RED' or message == 'WINNER_YELLOW':
                    if message == 'WINNER_RED':
                        print(username + ' WINS')
                        break
                    else:
                        print('COMPUTER WINS')
                        break
                else:
                    print('Invalid move.')
            except ConnectionError:
                print('Connection Error')