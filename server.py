# Include Python's Socket Library
from socket import *
from datetime import *

# Specify Server Port
serverPort = 12000

# Create TCP welcoming socket
serverSocket = socket(AF_INET, SOCK_STREAM)


def sendHtml(connectionSocket, resp):
    d = datetime.now()
    print(d)
    if resp == '200':
        connectionSocket.send(('HTTP/1.1 200 OK\r\n').encode())  # 1.0 should work as well 
        connectionSocket.send(('max-age=60\nExpires: Fri, 9 Apr 2021 17:47:04 PST\r\n').encode())
        connectionSocket.send(('Content-Type: text/html\r\n').encode())
        # header and body should be separated by additional newline
        
        connectionSocket.send(('\r\n').encode())
        connectionSocket.send(("""
            <html>
            <body>
            <h1 style='color:red'>Shit works</h1> yeeee
            </body>
            </html>
        """).encode())
    elif resp == '404':
        connectionSocket.send(('HTTP/1.1 404 Not Found\r\n').encode()
                            )
    elif resp == '304':
        connectionSocket.send(('HTTP/1.1 304 Not Modified\r\n').encode()
                            )
    elif resp == '400':
        connectionSocket.send(('HTTP/1.1 400 Bad Request\r\n').encode()
                            )
    elif resp == '408':
        connectionSocket.send(('HTTP/1.1 408 Request Timed Out\r\n').encode()
                            )

    # Close connectiion too client (but not welcoming socket)
    connectionSocket.close()




# Bind the server port to the socket
serverSocket.bind(('', serverPort))

# Server begins listerning foor incoming TCP connections
serverSocket.listen(1)
print('The server is ready to receive')

while True:  # Loop forever
    # Server waits on accept for incoming requests.
    # New socket created on return
    connectionSocket, addr = serverSocket.accept()

    # Read from socket (but not address as in UDP)
    sentence = connectionSocket.recv(1024).decode()
    req = sentence.split('\r\n', 1)
    location = req[0].split(' ')
    print('\n' + sentence)
    resp = '200'

    if location[1] == "/index.html" or location[1] == '/':
        # OK query
        print("OK")
    else:
        # asking for file that doesnt exist
        resp = "404"
        print("Not Found")
    # Send the reply
    sendHtml(connectionSocket, resp)


    