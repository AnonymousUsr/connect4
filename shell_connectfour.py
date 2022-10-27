from collections import namedtuple
import connectfour
import functions_connectfour

GameState = namedtuple('GameState', ['board', 'turn'])

def start_game() -> GameState:
    '''When called constructs a connect four game based on user inputs within a certain range
    Return - GameState (connect four game)'''
    newGame = None
    while newGame == None:
        userInput = input('Do you want to play a game of Connect Four?(yes/no) ')
        if userInput.lower() == 'yes':
            columnInput, rowInput = functions_connectfour.board_size()
            if (4 <= columnInput <= 20) and (4 <= rowInput <= 20):
                newGame = connectfour.new_game(columnInput, rowInput)
                return newGame
            else:
                print('Invalid values. Try again.')
        elif userInput.lower() == 'no':
            print('Have a nice day!')
            return GameState([[0]], '')
        else:
            print('Enter in yes or no')

def take_turn(game_state: GameState) -> GameState:
    '''Allows the user to make a valid move and prints/changes the board according to move
    Parameters - GameState (connect four game)
    Return - GameState (connect four game after a move is made)'''
    newGameState = game_state
    functions_connectfour.print_board(game_state)
    print('It is ' + functions_connectfour.whos_turn(game_state[1]) + '\'s turn')
    try:
        dropOrPop, turnInput = functions_connectfour.board_input()
        if dropOrPop.lower() == 'drop':
            newGameState = connectfour.drop(game_state, turnInput-1)
        elif dropOrPop.lower() == 'pop':
            newGameState = connectfour.pop(game_state, turnInput-1)
    except:
        print('InvalidMoveError: Try a different move.')
    finally:
        return newGameState

def until_winner(game_state: GameState) -> int:
    '''Repeats the connect four game until a winner is found and returns the winner
    Parameter - GameState (connect four game)
    Return - winner of the connect four game (as a number based on connectfour.py'''
    if (game_state != None):
        newGameState = take_turn(game_state)
        while connectfour.winner(newGameState) == 0:
            newGameState = take_turn(newGameState)
    else:
        newGameState = take_turn(game_state)
    functions_connectfour.print_board(newGameState)
    return(newGameState[1])

if __name__ == "__main__":
    '''If module is being run as main function, starts game until a winner is identified or no game is wanted'''
    startedGame = start_game()
    if startedGame[0] != [[0]]:
        winner = until_winner(startedGame)
        print(functions_connectfour.find_winner(winner))