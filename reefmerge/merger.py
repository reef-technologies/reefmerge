import logging

from reefmerge.resolvers.isort import ISortMerger
from reefmerge.resolvers.yapf import YapfMerger


class Merger(object):
    def __init__(self, conflict_handler):
        self._conflict_handler = conflict_handler

    def merge(self, dry_run=True):
        mergers_list = [ISortMerger, YapfMerger]  # TODO implement possibility to select mergers by user

        self._conflict_handler.read_originals()

        if not mergers_list:
            logging.error("No mergers selected to use")
            # FIXME should I call the default git merger now?
            return False

        for resolver in mergers_list:
            merger = resolver(self._conflict_handler)
            status, result, versions_dict = merger.merge()
            if status:
                logging.warning("The '%s' didn't solve the conflict" % str(merger))
            else:
                logging.warning("All conflicts resolved after '%s' intervention" % str(merger))
                break

            self._conflict_handler.update_contents(versions_dict=versions_dict)

        if dry_run:
            print(result)
        else:
            self._conflict_handler.save_resolution(result)

        return True
