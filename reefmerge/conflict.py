import os
import tempfile

from reefmerge.constants import Version


class Conflict(object):
    def __init__(self, contents):
        self.contents = contents

    def iter_contents(self):
        return self.contents.items()

    @classmethod
    def from_paths(cls, ancestor_filepath, mine_filepath, yours_filepath):
        paths = {
            Version.ANCESTOR: ancestor_filepath,
            Version.MINE: mine_filepath,
            Version.YOURS: yours_filepath,
        }
        return cls.from_paths_dict(paths)

    @classmethod
    def from_paths_dict(cls, paths_dict):
        contents = {}
        for version, file_path in paths_dict.items():
            with open(file_path, 'r') as fd:
                contents[version] = fd.read()
        return Conflict(contents=contents)


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
