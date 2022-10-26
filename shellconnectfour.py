from collections import namedtuple
import connectfour
import functions

GameState = namedtuple('GameState', ['board', 'turn'])

#When called constructs a connect four game based on user inputs within a certain range
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
            print('Have a nice day!')
            return GameState([[0]], '')
        else:
            print('Enter in yes or no')

GameState = namedtuple('GameState', ['board', 'turn'])

#If module is being run as main function, starts game until a winner is identified or no game is wanted
if __name__ == "__main__":
    startedGame = start_game()
    if startedGame[0] != [[0]]:
        winner = functions.until_winner(startedGame)
        print(functions.find_winner(winner))