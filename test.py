import random


class PlayerQueue:
    def __init__(self) -> None:
        self.queue = []
        self.index = -1

    def __check_queue(self, index):
        try:
            self.queue[index]
            return True
        except:
            return False
        
    def next(self):
        self.index += 1
        if self.__check_queue(self.index):
            return self.queue[self.index]
        else:
            self.index -= 1
            return None

    def previous(self):
        self.index -= 1
        if self.__check_queue(self.index):
            return self.queue[self.index]
        else:
            self.index += 1
            return None
        
    def shuffle(self):
        upcoming = self.queue[self.index+1:]
        past = self.queue[:self.index+1]

        random.shuffle(upcoming)
        random.shuffle(past)

        self.queue = past+upcoming
        
        
    def clear(self):
        self.queue = []
        self.index = -1


queue = PlayerQueue()
queue.queue = [
   0, 1, 2, 3, 4, 5, 6, 7, 8, 9
]

print(queue.next())
print(queue.next())
print(queue.next())
print(queue.next())
print(queue.next())
print(queue.next())

queue.shuffle()
print(queue.queue)
