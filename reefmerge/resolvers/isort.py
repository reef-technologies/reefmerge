from isort import SortImports

from reefmerge.conflict import Temporal
from reefmerge.git_wrapper import GitWrapper
from reefmerge.resolvers.base import BaseMerger


class ISortMerger(BaseMerger):
    def __init__(self, conflict):
        super(ISortMerger, self).__init__(conflict)

    def merge(self):
        contents_isorted = {
            version: SortImports(file_contents=content).output
            for version, content in self._conflict.iter_contents()
        }

        temporal = Temporal(contents_isorted)
        status, out, err = GitWrapper.merge_file(temporal.locations)
        temporal.remove_all()

        return status, out, contents_isorted
