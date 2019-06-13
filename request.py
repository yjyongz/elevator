import time
class Request:
    def __init__(self, floor):
        self.floor = floor
        self.timestamp = int(time.time())

    def __gt__(self, request):
        return self.timestamp - request.timestamp > 0

    def __lt__(self, request):
        return self.timestamp - request.timestamp < 0
