import os
import pytest

from reefmerge.files_handler import Files
from reefmerge.merger import ISortMerger

ISORT_MERGER_TEST_FILES_PATH = os.path.join("tests", "files", "isort")


@pytest.mark.parametrize("path", [
    "permuted_imports",
])
def test_merge(path):
    files, result_file = _files_obj_generator(path)
    files.read_originals()

    result = ISortMerger(files).merge()

    with open(result_file, 'r') as rfd:
        expected_content = rfd.read()

    if not result.endswith('\n'):
        result = "{}\n".format(result)  # workaround for isort forgotting about \n at EOF

    assert expected_content == result


def _files_obj_generator(files_set_name):
    files_location = os.path.join(ISORT_MERGER_TEST_FILES_PATH, files_set_name)
    files = Files(
        ancestor=os.path.join(files_location, "ancestor.py"),
        mine=os.path.join(files_location, "mine.py"),
        yours=os.path.join(files_location, "yours.py")
    )
    return files, os.path.join(files_location, "result.py")
