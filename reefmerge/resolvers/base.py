
class BaseMerger(object):
    def __init__(self, files):
        self._files = files

    def merge(self):
        raise NotImplementedError("Implemented in subclass")
