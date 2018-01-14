from reefmerge.resolvers.isort import ISortMerger


class Merger(object):
    def __init__(self, conflict_handler):
        self._conflict_handler = conflict_handler

    def merge(self, dry_run=True):
        self._conflict_handler.read_originals()
        # TODO standard merge-driver run? WARNING what if this will cause a infinity loop?
        result = ISortMerger(self._conflict_handler).merge()  # FIXME what should happen with result?
        # TODO yapf resolver
        # TODO end-point additions resolver
        # TODO ... more resolvers?

        if dry_run:
            print(result)
        else:
            self._conflict_handler.save_resolution(result)

        return True
