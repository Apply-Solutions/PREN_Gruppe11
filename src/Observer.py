from abc import abstractmethod, ABCMeta


class Observer:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def update(self, message):
        pass
