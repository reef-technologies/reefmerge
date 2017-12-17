from reefmerge.resolvers.isort import ISortMerger


class Merger(object):
    def __init__(self, files):
        self._files = files

    def merge(self, dry_run=True):
        self._files.read_originals()
        # TODO standard merge-driver run? WARNING what if this will cause a infinity loop?
        result = ISortMerger(self._files).merge()  # FIXME what should happen with result?
        # TODO yapf resolver
        # TODO end-point additions resolver
        # TODO ... more resolvers?

        if dry_run:
            print(result)
        else:
            self._files.save_result(result)

        return True
