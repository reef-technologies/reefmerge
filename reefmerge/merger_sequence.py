import logging

from reefmerge.git_wrapper import GitWrapper

from reefmerge.resolvers.isort import ISortMerger
from reefmerge.resolvers.yapf import YapfMerger


class MergerSequence(object):
    def __init__(self, conflict_handler, mergers_list):
        self._conflict_handler = conflict_handler
        self._mergers_list = mergers_list
        self._mergers_list = [ISortMerger, YapfMerger]  # TODO implement possibility to select mergers by user

    def merge(self, dry_run=True):
        self._conflict_handler.read_originals()

        result = None
        for resolver in self._mergers_list:
            merger = resolver(self._conflict_handler)
            status, result, versions_dict = merger.merge()
            if status:
                logging.warning("The '%s' didn't solve the conflict", str(merger))
            else:
                logging.warning("All conflicts resolved after '%s' intervention", str(merger))
                break

            self._conflict_handler.update_contents(versions_dict=versions_dict)

        if not result:
            result = GitWrapper.merge_file(self._conflict_handler.contents)

        if dry_run:
            print(result)
        else:
            self._conflict_handler.save_resolution(result)

        return True
