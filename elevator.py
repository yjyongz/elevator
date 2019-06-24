import time
import threading
from floor import Firstfloor
from floor import Lastfloor
from floor import Floor
from floor import Direction
from operator import add
from operator import sub
from rrequest import OutDoorRequest
from rrequest import InDoorRequest

class Elevator:
    def __init__(self, floors, index, mmin, mmax):
        self.floors = []
        for idx in range(floors):
            if idx == 0:
                self.floors.append(Firstfloor(idx, Direction.NONE))
            elif idx == floors - 1:
                self.floors.append(Lastfloor(idx, Direction.NONE))
            else:
                self.floors.append(Floor(idx, Direction.NONE, Direction.NONE))
        self.index = index # elevator index
        self.lock = threading.Lock()
        self.cv = threading.Condition(self.lock)
        self.current_floor = 0
        self.min_floor = mmin
        self.max_floor = mmax
        self.direction = Direction.UP
        self.num_of_request = 0
        t1 = threading.Thread(target=self.move, args=())
        t1.start()

    def addRequest(self, request):
        if isinstance(request, OutDoorRequest):
            floor, direction = request.floor, request.direction
        elif isinstance(request, InDoorRequest):
            floor = request.floor
            if floor - self.current_floor > 0:
                direction = Direction.UP
            elif floor - self.current_floor < 0:
                direction = Direction.DOWN
            else:
                direction = Direction.UP
        else:
            raise Exception("invalid request")

        if direction == Direction.UP:
            self.floors[floor].updirection = direction 
            if 0 != floor != self.max_floor:
                self.floors[floor].uphasStop = 1
            else:
                self.floors[floor].hasStop = 1
        elif direction == Direction.DOWN:
            self.floors[floor].downdirection = direction
            if 0 != floor != self.max_floor:
                self.floors[floor].downhasStop = 1
            else:
                self.floors[floor].hasStop = 1
            
        self.num_of_request += 1
        print ("number of request: ",self.num_of_request)
        with self.cv:
            self.cv.notify() 

    def hasMoreFloor(self, current_floor, direction):
        if direction == Direction.UP:
            for idx in range(current_floor+1, self.max_floor, 1):
                if idx == self.max_floor - 1 and self.floors[idx].hasStop == 1:
                    return True
                elif idx != self.max_floor-1 and self.floors[idx].uphasStop == 1:
                    return True
            return False
        elif direction == Direction.DOWN:
            for idx in range(current_floor-1, self.min_floor, -1):
                if idx == self.min_floor and self.floors[idx].hasStop == 1:
                    return True
                elif idx != self.min and self.floors[idx].downhasStop == 1:
                    return True
            return False

    def move(self):
        with self.lock:
            while True:
                while self.num_of_request == 0:
                    self.cv.wait()
                print (self.direction, Direction.UP, Direction.UP == self.direction)
                direction = self.direction
                sDir = "None"
                if direction == Direction.UP:
                    func = add
                    sDir = "UP"
                    startFloor = self.current_floor
                    endFloor = self.max_floor
                    step = 1
                elif direction == Direction.DOWN:
                    func = sub
                    sDir = "DOWN"
                    startFloor = self.current_floor
                    endFloor = self.min_floor
                    step = -1
                print (sDir, " ", startFloor, endFloor, step)
                for floor in range(startFloor+step, endFloor, step):
                    time.sleep(1)
                    obj = self.floors[floor]
                    print ("going ", sDir, " current floor ", self.current_floor)
                    iflag = False
                    if isinstance(obj, Firstfloor) and obj.hasStop == 1 and obj.updirection == direction:
                        print (" ".join(["Stoped at", str(floor)]))
                        self.num_of_request -= 1
                        obj.updirection = Direction.NONE
                        obj.hasStop = 0
                        iflag = True
                    elif isinstance(obj, Lastfloor) and obj.hasStop == 1 and obj.downdirection == direction:
                        print (" ".join(["Stoped at", str(floor)]))
                        self.num_of_request -= 1
                        obj.downdirection = Direction.NONE
                        obj.hasStop = 0
                        iflag = True
                    elif isinstance(obj, Floor) and obj.uphasStop == 1 and obj.updirection == direction:
                        print (" ".join(["Stoped at", str(floor)]))
                        self.num_of_request -= 1
                        obj.updirection = Direction.NONE
                        self.uphashstop = 0
                        iflag = True
                    elif isinstance(obj, Floor) and obj.downhasStop == 1 and obj.downdirection == direction:
                        print (" ".join(["Stoped at", str(floor)]))
                        self.num_of_request -= 1
                        obj.downdirection = Direction.NONE
                        self.downhashstop = 0
                        iflag = True

                    self.current_floor = floor
                    print ("DD ",self.direction, iflag)
                    if self.num_of_request == 0:
                        break
                    if iflag and not self.hasMoreFloor(self.current_floor, direction):
                        if floor == self.max_floor - 1:
                            self.direction = Direction.DOWN
                        elif floor == self.min_floor:
                            self.direction = Direction.UP
                        else:
                            if direction == Direction.DOWN:
                                self.direction = Direction.UP
                            else:
                                self.direction = Direction.DOWN
                        break
