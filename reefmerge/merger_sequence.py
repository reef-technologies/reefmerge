import logging

from reefmerge.git_wrapper import GitWrapper

from reefmerge.resolvers.isort import ISortMerger
from reefmerge.resolvers.yapf import YapfMerger


class MergerSequence(object):
    def __init__(self, conflict, mergers_list):
        self._conflict = conflict
        self._mergers_list = mergers_list
        self._mergers_list = [ISortMerger, YapfMerger]  # TODO implement possibility to select mergers by user

    def merge(self, dry_run=True):
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

            self._conflict.update_contents(versions_dict=versions_dict)

        if not result:
            result = GitWrapper.merge_file(self._conflict.contents)

        if dry_run:
            print(result)
        else:
            self._conflict.save_resolution(result)

        return True
