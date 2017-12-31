import os
import tempfile

from reefmerge.constants import Version


class ConflictHandler(object):
    def __init__(self, ancestor_filepath, mine_filepath, yours_filepath):
        self._paths = {
            Version.ANCESTOR: ancestor_filepath,
            Version.MINE: mine_filepath,
            Version.YOURS: yours_filepath,
        }
        self._opened = {}
        self._originals = {}

    def read_originals(self):
        for version, file_path in self._paths.items():
            with open(file_path, 'r') as fd:
                self._originals[version] = fd.read()

    def iter_originals(self):
        return self._originals.items()

    def save_resolution(self, content):
        with open(self._paths[Version.MINE], 'w') as fd:
            fd.write(content)


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
