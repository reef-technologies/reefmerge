
class BaseMerger(object):
    def __init__(self, conflict_handler):
        self._conflict_handler = conflict_handler

    def merge(self):
        raise NotImplementedError("Implemented in subclass")
