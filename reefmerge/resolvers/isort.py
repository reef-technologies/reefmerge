from isort import SortImports

from reefmerge.files_handler import Temporal
from reefmerge.git_wrapper import GitWrapper
from reefmerge.resolvers.base import BaseMerger


class ISortMerger(BaseMerger):
    def __init__(self, files):
        super(ISortMerger, self).__init__(files)

    def merge(self):
        contents_isorted = {
            version: SortImports(file_contents=content).output for version, content in self._files.iter_originals()
        }

        temporal = Temporal(contents_isorted)
        status, out, err = GitWrapper.merge_file(temporal.locations)
        temporal.remove_all()

        if status:
            print("There is still conflict")

        return out
