#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#
import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.PAIR)
socket.connect("ipc://test1")

#  Do 10 requests, waiting each time for a response
for request in range(1, 10):
    #  Get the reply.
    message = socket.recv()
    print("Received reply ", request, "[", message, "]")

    print("Sending request ", request, "...")
    socket.send_string("Hello")
