
class BaseMerger(object):
    def __init__(self, conflict_handler):
        self._conflict_handler = conflict_handler

    def __str__(self):
        return self.__class__.__name__

    def merge(self):
        raise NotImplementedError("Implemented in subclass")
