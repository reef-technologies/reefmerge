import os

from reefmerge.conflict_handler import ConflictHandler


def create_conflict_handler(files_set_name, path):
    files_location = os.path.join(path, files_set_name)
    conflict_handler = ConflictHandler(
        ancestor_filepath=os.path.join(files_location, "ancestor.py"),
        mine_filepath=os.path.join(files_location, "mine.py"),
        yours_filepath=os.path.join(files_location, "yours.py"),
    )
    return conflict_handler, os.path.join(files_location, "result.py")
