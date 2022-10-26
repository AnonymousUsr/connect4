import socket
from collections import namedtuple
import functions

Connection = namedtuple('Sockets', ['openedSocket', 'inputSocket', 'outputSocket'])

def open_socket(host: str, port: int) -> Connection:
    openedSocket = socket.socket()
    connectAddress = (host, port)
    openedSocket.connect(connectAddress)
    openedSocketInput = openedSocket.makefile('r')
    openedSocketOutput = openedSocket.makefile('w')

    return Connection(openedSocket, openedSocketInput, openedSocketOutput)

def close_socket(connectedSocket: Connection) -> None:
    for item in connectedSocket:
        item.close()
    
def send(connectedSocket: Connection, message: str) -> None:
    connectedSocket[2].write(message + '\r\n')
    connectedSocket[2].flush()

def receive(connectedSocket: Connection) -> None:
    return connectedSocket[1].readline()[:-1]

def what_host() -> str:
    while True:
        host = input('Input Host: ').strip()
        if host == '':
            print('Try again: ')
        else:
            return host

def what_port() -> int:
    try:
        port = int(input('Input port: '))
        if 0 <= port <= 65535:
            return port
        else:
            print('Invalid port. Port must be between 0 and 65535')
    except ValueError:
        pass

def run_protocol(username: str, columns: int, rows: int, counter: int) -> str:
    try:
        if counter == 0:
            host = what_host()
            port = what_port()

            connectedSocket = open_socket(host, port)
            send(connectedSocket, 'I32CFSP_HELLO ' + username)
            response = receive(connectedSocket)
            print(response)
            send(connectedSocket, 'AI_GAME ' + str(columns) + ' ' + str(rows))
            response = receive(connectedSocket)
            counter += 1
        
        dropOrPop = input('Do you want to drop or pop a piece? ')
        turnInput = int(input('Choose a column '))
        send(connectedSocket, dropOrPop.upper() + ' ' + str(turnInput))
        response = receive(connectedSocket)
        response2 = receive(connectedSocket)
        response3 = receive(connectedSocket)
        print('Computer Move: ' + response2)
        return dropOrPop, turnInput, response, response2, response3, counter
        
    except:
        print('Invalid socket input')
    close_socket(connectedSocket)
    return connectedSocket