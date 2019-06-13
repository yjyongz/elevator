import time
from enum import Enum
import heapq
import threading

class Door(Enum):
    CLOSE = 0
    OPEN = 1

class Direction(Enum):
    UP = 0
    DOWN = 1

class Elevator:
    def __init__(self, floors, index):
        self.floors = floors
        self.cur_request = []
        self.up_request = []
        self.down_request = []
        self.floor = 0
        self.direction = Direction.UP
        self.index = index
        self.lock = threading.Lock()

    def processMove(self):
        self.lock.acquire()
        print ("calling processMove")
        self.move()
        self.lock.release()

    def addRequest(self, request):
        if self.floor - request.floor < 0: 
            # going up
            heapq.heappush(self.up_request, request)
            self.cur_request = self.up_request
        elif self.floor - request.floor > 0:
            # going down`
            heapq.heappush(self.down_request, request)
            self.cur_request = self.down_request
        t1 = threading.Thread(target=self.processMove, args=())
        t1.start()
    
    def move(self):
        item = heapq.heappop(self.cur_request)
        targetFloor, timestamp = item.floor, item.timestamp
        if self.floor - targetFloor < 0: 
            # going up
            self.direction = Direction.UP
            sMOVE = "UP"
        elif self.floor - targetFloor > 0:
            # going down
            self.direction = Direction.DOWN
            sMOVE = "DOWN"
        else:
            return

        while self.floor != targetFloor:
            time.sleep(1)
            if self.direction == Direction.UP:
                self.floor += 1
            else:
                self.floor -= 1
            print (self.index, " ", "going  ", sMOVE, " ", self.floor)
