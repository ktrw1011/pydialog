import abc

class BaseSystem(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractclassmethod
    def initial_message(self, input):
        raise NotImplementedError

    @abc.abstractclassmethod
    def reply(self, input):
        raise NotImplementedError