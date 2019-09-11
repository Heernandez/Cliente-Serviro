import zmq

from random import randrange

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

i = 0
while True:
    zipCode = randrange(1,100000)
    temperature = randrange(-80,135)
    relHumidity = randrange(10,60)

    if zipCode == 10001:
        print("publicacion de ",temperature)

    socket.send_string("%i %i %i" %(zipCode,temperature,relHumidity))

    i += 1