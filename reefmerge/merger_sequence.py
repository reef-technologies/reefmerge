import logging

from reefmerge.conflict import Conflict
from reefmerge.git_wrapper import GitWrapper


class MergerSequence(object):
    def __init__(self, conflict, mergers_list):
        self._conflict = conflict
        self._mergers_list = mergers_list

    def merge(self):
        self._conflict.read_originals()

        result = None
        for resolver in self._mergers_list:
            merger = resolver(self._conflict)
            status, result, versions_dict = merger.merge()
            if status:
                logging.warning("The '%s' didn't solve the conflict", str(merger))
            else:
                logging.warning("All conflicts resolved after '%s' intervention", str(merger))
                break

            self._conflict = Conflict(contents=versions_dict)

        if not result:
            result = GitWrapper.merge_file(self._conflict.contents)

        return result
