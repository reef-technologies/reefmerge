import os

from reefmerge.conflict import Conflict


def create_conflict_handler(files_set_name, path):
    files_location = os.path.join(path, files_set_name)
    conflict = Conflict.from_paths(
        ancestor_filepath=os.path.join(files_location, "ancestor.py"),
        mine_filepath=os.path.join(files_location, "mine.py"),
        yours_filepath=os.path.join(files_location, "yours.py"),
    )
    return conflict, os.path.join(files_location, "result.py")
