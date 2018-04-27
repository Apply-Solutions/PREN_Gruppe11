from abc import abstractmethod, ABCMeta


class Observerable:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def update(self, message):
        pass
