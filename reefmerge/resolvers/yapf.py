from yapf import yapf_api

from reefmerge.conflict_handler import Temporal
from reefmerge.git_wrapper import GitWrapper
from reefmerge.resolvers.base import BaseMerger


class YapfMerger(BaseMerger):
    def __init__(self, conflict_handler):
        super(YapfMerger, self).__init__(conflict_handler)

    def __repr__(self):
        return "YAPF merger"

    def merge(self):
        contents_yapfed = {
            version: yapf_api.FormatCode(content)[0]
            for version, content in self._conflict_handler.iter_contents()
        }

        temporal = Temporal(contents_yapfed)
        status, out, err = GitWrapper.merge_file(temporal.locations)
        temporal.remove_all()

        return status, out, contents_yapfed
