import git

from reefmerge.constants import Version


class GitWrapper(object):
    def __init__(self):
        pass

    @classmethod
    def merge_file(cls, files_dct):
        files_list = [
            files_dct[Version.MINE],
            files_dct[Version.ANCESTOR],
            files_dct[Version.YOURS],
        ]
        command = ["git", "merge-file", "-p"]
        command.extend(files_list)

        g = git.Git()
        return g.execute(
            command=command,
            with_extended_output=True,
            with_exceptions=False,
        )
