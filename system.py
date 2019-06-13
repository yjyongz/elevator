import threading
from elevator import Elevator
from request import Request
import signal
import sys

active = True
def ctrl_c_hdlr(signum, frame):
    print ("sig handlered")
    global active
    active = False
    sys.exit(0)

signal.signal(signal.SIGINT, ctrl_c_hdlr)
class system:
    def __init__(self, N=4, floors=50):
        self.number_of_elevators = N
        self.elevators = [Elevator(floors, idx) for idx in range(N)]

building = system()

while active:
    try:
        result = input().split()
        index, floor = result[0], result[1]
        if floor.isdigit() and index.isdigit():
            index, floor = int(index), int(floor)
            building.elevators[index].addRequest(Request(floor))
        else:
            print ("invalid input")
    except Exception as e:
        print ("2 invalid input ", e)
