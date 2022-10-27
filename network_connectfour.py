
from collections import namedtuple
import sockets_connectfour
import functions_connectfour
import connectfour

GameState = namedtuple('GameState', ['board', 'turn'])
Connection = namedtuple('Sockets', ['openedSocket', 'inputSocket', 'outputSocket'])

def start_game():
    '''Creates a board for the connect four game
    Return - connect four game, number of columns and rows'''
    newGame = None
    while newGame == None:
            columnInput, rowInput = functions_connectfour.board_size()
            if (4 <= columnInput <= 20) and (4 <= rowInput <= 20):
                newGame = connectfour.new_game(columnInput, rowInput)
                return newGame, columnInput, rowInput
            else:
                print('Invalid values. Try again.')

def find_space(text: str) -> bool:
    '''Checks if there is any whitespace in a given string
    Parameters - given text
    Return - Does the text have any whitespace inside'''
    for letter in text.strip():
        if letter == (' ') or letter == ('   '):
            return True
    return False

def game_results(startedGame: GameState) -> None:
    '''Runs through the connect four game until a winner is found, then prints the winner
    Parameter - GameState of connect four game'''
    while connectfour.winner(startedGame) == 0:
        try:
            move, col, message, message2, message3 = run_protocol(connection)
            if message2 != 'INVALID' and move != '':
                if message[0:6] == 'WINNER':
                    break
                startedGame = player_move(move, col, startedGame)
                splitMessage = message2.split(' ')
                if len(splitMessage) == 2:
                    startedGame = player_move(splitMessage[0], int(splitMessage[1]), startedGame)
                    print('Computer Move: ' + message2)
                functions_connectfour.print_board(startedGame)
            else:
                print('Invalid move.')
        except ConnectionError:
            print('Connection Error')
    if message3[0:6] == 'WINNER':
        functions_connectfour.print_board(startedGame)
        print(functions_connectfour.find_winner(message3))
    elif message != None:
        functions_connectfour.print_board(startedGame)
        print(functions_connectfour.find_winner(message))
    
def player_move(move: str, col: int, game_state: GameState) -> GameState:
    '''Takes player inputs and changes and prints the connect four board accordingly
    Parameters - player move (drop or pop), column, GameState (connect four game)
    Return - GameState after move is made in the column given'''
    newGameState = game_state
    try:
        if move.lower() == 'drop':
            newGameState = connectfour.drop(game_state, col-1)
            print('It is ' + functions_connectfour.whos_turn(game_state[1]) + '\'s turn')
        elif move.lower() == 'pop':
            newGameState = connectfour.pop(game_state, col-1)
            print('It is ' + functions_connectfour.whos_turn(game_state[1]) + '\'s turn')
    except:
        print('InvalidMoveError: Try a different move.')
    finally:
        return newGameState

def run_protocol(connectedSocket: Connection) -> str:
    '''Takes moves from the user, sends it to the server, and returns the received messages from the server
    Parameter - connection to a server
    Return - player move (drop or pop), column, up to 3 possible messages received from the server'''
    dropOrPop, turnInput = functions_connectfour.board_input()
    if dropOrPop.upper() == 'DROP' or dropOrPop.upper() == 'POP': 
        try:
            sockets_connectfour.send(connectedSocket, dropOrPop.upper() + ' ' + str(turnInput))
            response = sockets_connectfour.receive(connectedSocket)
            if response == 'WINNER_RED' or response == 'WINNER_YELLOW':
                return dropOrPop, turnInput, response, '', ''
            elif response != 'WINNER_RED' or response != 'WINNER_YELLOW':
                response2 = sockets_connectfour.receive(connectedSocket)
                response3 = ''
            if response != 'INVALID':
                response3 = sockets_connectfour.receive(connectedSocket)
            return dropOrPop, turnInput, response, response2, response3
        except:
            print('Invalid input.')
    else:
        print('You can only drop or pop a piece.')
        return '', -1, '', '', ''
    
if __name__ == '__main__':
    '''If module is being run as main function, starts game of connect four'''
    username = (input('Enter a username(no spaces): ')).strip()
    if not find_space(username):
        startedGame, columns, rows = start_game()
        connection = sockets_connectfour.open_protocol(username, columns, rows)
        if connection != None:
            print('YOU ARE RED')
            game_results(startedGame)
