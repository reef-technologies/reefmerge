from yapf import yapf_api

from reefmerge.conflict import Temporal
from reefmerge.git_wrapper import GitWrapper
from reefmerge.resolvers.base import BaseMerger


class YapfMerger(BaseMerger):
    def __init__(self, conflict):
        super(YapfMerger, self).__init__(conflict)

    def merge(self):
        contents_yapfed = {
            version: yapf_api.FormatCode(content)[0]
            for version, content in self._conflict.iter_contents()
        }

        temporal = Temporal(contents_yapfed)
        status, out, err = GitWrapper.merge_file(temporal.locations)
        temporal.remove_all()

        return status, out, contents_yapfed
