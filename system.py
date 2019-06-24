from elevator import Elevator
from rrequest import OutDoorRequest
from rrequest import InDoorRequest
import time
from floor import Direction

active = True
class system:
    def __init__(self, N=4, floors=50):
        self.number_of_elevators = N
        self.elevators = [Elevator(floors, idx, 0, floors) for idx in range(N)]

building = system()

while active:
    try:
        result = input().split()
        index, floor, direction = result[0], result[1], result[2]
        if floor.isdigit() and index.isdigit() and direction.isdigit():
            index, floor, direction = int(index), int(floor), int(direction)
            if direction == 0:
                direction = Direction.UP
            else:
                direction = Direction.DOWN
            building.elevators[index].addRequest(OutDoorRequest(floor, direction))
        else:
            print ("invalid input")
    except Exception as e:
        print ("2 invalid input ", e)
