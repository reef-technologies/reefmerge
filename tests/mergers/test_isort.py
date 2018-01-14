import os
import pytest

from reefmerge.resolvers.isort import ISortMerger
from tests.mergers.common import default_merger_test

ISORT_MERGER_TEST_FILES_PATH = os.path.join("tests", "files", "isort")


@pytest.mark.parametrize("path", [
    "permuted_imports",
])
def test_merge(path):
    default_merger_test(ISortMerger, path, ISORT_MERGER_TEST_FILES_PATH)
