import logging

from reefmerge.conflict import Conflict
from reefmerge.git_wrapper import GitWrapper


class MergerSequence(object):
    def __init__(self, paths, mergers_list):
        self._paths = paths
        self._mergers_list = mergers_list

    def merge(self):
        conflict = Conflict.from_paths_dict(self._paths)

        result = None
        for resolver in self._mergers_list:
            merger = resolver(conflict)
            status, result, versions_dict = merger.merge()
            if status:
                logging.warning("The '%s' didn't solve the conflict", str(merger))
            else:
                logging.warning("All conflicts resolved after '%s' intervention", str(merger))
                break

            conflict = Conflict(contents=versions_dict)

        if not result:
            _, result, _ = GitWrapper.merge_file(conflict.contents)

        return result
