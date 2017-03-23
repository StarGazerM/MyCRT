#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects "Hello" from client, replies with "World"
#
import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("ipc://test1")

while True:
    #  Send reply back to client
    socket.send_string("World")

    #  Wait for next request from client
    message = socket.recv()
    print("Received request: ", message)

    #  Do some 'work'
    time.sleep(1)  # Do some 'work'
