import os
import pytest

from reefmerge.conflict_handler import ConflictHandler
from reefmerge.merger import ISortMerger

ISORT_MERGER_TEST_FILES_PATH = os.path.join("tests", "files", "isort")


@pytest.mark.parametrize("path", [
    "permuted_imports",
])
def test_merge(path):
    conflict_handler, result_file = _create_conflict_handler(path)
    conflict_handler.read_originals()

    result = ISortMerger(conflict_handler).merge()

    with open(result_file, 'r') as rfd:
        expected_content = rfd.read()

    if not result.endswith('\n'):
        result = "{}\n".format(result)  # workaround for isort forgotting about \n at EOF

    assert expected_content == result


def _create_conflict_handler(files_set_name):
    files_location = os.path.join(ISORT_MERGER_TEST_FILES_PATH, files_set_name)
    conflict_handler = ConflictHandler(
        ancestor_filepath=os.path.join(files_location, "ancestor.py"),
        mine_filepath=os.path.join(files_location, "mine.py"),
        yours_filepath=os.path.join(files_location, "yours.py"),
    )
    return conflict_handler, os.path.join(files_location, "result.py")
