import os
import tempfile

from reefmerge.constants import Version


class Conflict(object):
    def __init__(self, contents=None):
        self._paths = None
        self.contents = contents

    def read_originals(self):
        for version, file_path in self._paths.items():
            with open(file_path, 'r') as fd:
                self.contents[version] = fd.read()

    def iter_contents(self):
        return self.contents.items()

    def update_contents(self, versions_dict):
        self.contents = versions_dict

    @classmethod
    def from_paths(cls, ancestor_filepath, mine_filepath, yours_filepath):
        conflict = Conflict()
        conflict._paths = {
            Version.ANCESTOR: ancestor_filepath,
            Version.MINE: mine_filepath,
            Version.YOURS: yours_filepath,
        }
        conflict.contents = {}
        return conflict


class Temporal(object):
    def __init__(self, files_contents):
        self.locations = {}
        for version, content in files_contents.items():
            fd, file_name = tempfile.mkstemp()
            self.locations[version] = file_name
            with os.fdopen(fd, 'w') as opened:
                opened.write(content)

    def remove_all(self):
        for _, file_name in self.locations.items():
            os.remove(file_name)
