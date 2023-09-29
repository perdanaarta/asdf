from enum import Enum
import random

class QueueLoop(Enum):
    NONE = 0
    ALL = 1
    ONE = 2


class Queue:
    def __init__(self) -> None:
        self.__queue = []    
        self.index = -1
        self.loop = QueueLoop.NONE
        
    def __check_queue(self, index):
        try:
            self.__queue[index]
            return True
        except:
            return False

    def __get(self, index):
        try:
            return self.__queue[index]
        except:
            return None

    @property
    def upcoming(self):
        return self.__queue[self.index+1:]

    @property
    def history(self):
        return self.__queue[:self.index]

    @property
    def current(self):
        if self.__check_queue(self.index):
            return self.__queue[self.index]
        else:
            return None
        
    def put(self, item):
        if isinstance(item, list):
            upcoming = self.upcoming + item
        else:
            upcoming = self.upcoming.append(item)
        self.__queue = self.history + [self.current] if self.current is not None else [] + upcoming

    def put_front(self, item):
        if isinstance(item, list):
            upcoming = item + self.upcoming
        else:
            upcoming = self.upcoming.insert(0, item)
        self.__queue = self.history + [self.current] if self.current is not None else [] + upcoming
        
    def next(self):
        if self.loop == QueueLoop.ALL:
            if not self.__check_queue(self.index+1):
                self.index = 0
                return self.__get(self.index)
            
        if self.loop == QueueLoop.ONE:
            if self.index < 0:
                self.index = 0
            return self.__get(self.index)

        else:
            if self.__check_queue(self.index+1):
                self.index += 1
                return self.__get(self.index)

    def previous(self):
        if self.__check_queue(self.index+1):
            return self.__get(self.index)
        else:
            return None

    def shuffle(self):
        """Shuffle the queue"""
        upcoming = self.upcoming
        history = self.history

        random.shuffle(upcoming)
        random.shuffle(history)

        self.__queue = history + [self.current] + upcoming

    def clear(self):
        self.__queue = []
        self.index = -1

    @property
    def loop(self):
        return self.__loop

    @loop.setter
    def loop(self, value: QueueLoop) -> None:
        if not isinstance(value, QueueLoop):
            raise ValueError('The "loop" property can only be set with QueueLoop.')

        self.__loop = value