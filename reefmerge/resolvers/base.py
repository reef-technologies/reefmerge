
class BaseMerger(object):
    def __init__(self, conflict):
        self._conflict = conflict

    def __str__(self):
        return self.__class__.__name__

    def merge(self):
        raise NotImplementedError("Implemented in subclass")
