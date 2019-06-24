import time

class OutDoorRequest:
    def __init__(self, floor, direction):
        self.floor = floor
        self.direction = direction
        self.timestamp = int(time.time())

    def __gt__(self, request):
        return self.floor - request.floor > 0

class InDoorRequest:
    def __init__(self, targetFloor, direction, emergency = False):
        self.floor = targetFloor
        self.timestamp = int(time.time())

    def __gt__(self, request):
        return self.floor - request.floor > 0
