import time

class Shared():
    def __init__(self):
        self.shared_time = time.clock()
        
    def get_shared_time():
        return self.shared_time