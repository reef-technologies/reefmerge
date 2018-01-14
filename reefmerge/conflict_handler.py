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
        self._contents = {}

    def read_originals(self):
        for version, file_path in self._paths.items():
            with open(file_path, 'r') as fd:
                self._contents[version] = fd.read()

    def iter_contents(self):
        return self._contents.items()

    def update_contents(self, ancestor_version=None, mine_version=None, yours_version=None, versions_dict=None):
        if versions_dict:
            self._contents = versions_dict
        else:
            if ancestor_version:
                self._contents[Version.ANCESTOR] = ancestor_version
            if mine_version:
                self._contents[Version.MINE] = mine_version
            if yours_version:
                self._contents[Version.YOURS] = yours_version

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
