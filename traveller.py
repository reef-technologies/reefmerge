class Traveller(object):
    def __init__(self, ancestor_tree, current_tree, diff_tree):
        self._ancestor_tree = ancestor_tree
        self._current_tree = current_tree
        self._diff_tree = diff_tree

    def travel(self):
        return self._current_tree
