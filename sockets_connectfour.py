import socket
from collections import namedtuple

Connection = namedtuple('Sockets', ['openedSocket', 'inputSocket', 'outputSocket'])

def open_socket(host: str, port: int) -> Connection:
    '''opens the socket and creates pseudofiles to message a server
    Parameters - website/ip address and port
    Return - Connection with the opened socket and pseudo file'''
    openedSocket = socket.socket()
    connectAddress = (host, port)
    openedSocket.connect(connectAddress)
    openedSocketInput = openedSocket.makefile('r')
    openedSocketOutput = openedSocket.makefile('w')

    return Connection(openedSocket, openedSocketInput, openedSocketOutput)

def close_socket(connectedSocket: Connection) -> None:
    '''Closes the socket
    Parameter - Connection - opened socket'''
    for item in connectedSocket:
        item.close()
    
def send(connectedSocket: Connection, message: str) -> None:
    '''Sends a message to a server
    Parameter - connected socket, message to send to said socket'''
    connectedSocket[2].write(message + '\r\n')
    connectedSocket[2].flush()

def receive(connectedSocket: Connection) -> None:
    '''Receives a message from a server
    Parameter - connected socket
    Return - message from server'''
    return connectedSocket[1].readline()[:-1]

def what_host() -> str:
    '''Takes user input to determine the host of a server
    Return - user-inputted host'''
    while True:
        host = input('Input Host: ').strip()
        if host == '':
            print('Try again: ')
        else:
            return host

def what_port() -> int:
    '''Takes user input to determine the port of a server
    Return - valid user-inputted port'''
    try:
        port = int(input('Input port: '))
        if 0 <= port <= 65535:
            return port
        else:
            print('Invalid port. Port must be between 0 and 65535')
    except ValueError:
        pass

def open_protocol(username: str, columns: int, rows: int) -> Connection:
    '''Asks user for input to connect to a certain server 
    Then runs a protocol for the specific ICS connect four server
    host: circinus-32.ics.uci.edu, port: 4444
    Parameter - user's username, wanted columns and rows
    Return - connection to a server based on inputted host and port'''
    try:
        host = what_host()
        port = what_port()
        connectedSocket = open_socket(host, port)
        send(connectedSocket, 'I32CFSP_HELLO ' + username)
        response = receive(connectedSocket)
        print(response)
        send(connectedSocket, 'AI_GAME ' + str(columns) + ' ' + str(rows))
        response = receive(connectedSocket)
        return connectedSocket
    except:
        print('Invalid socket input')
        return None