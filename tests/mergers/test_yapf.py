import os
import pytest

from reefmerge.resolvers.yapf import YapfMerger
from tests.mergers.common import default_merger_test

YAPF_MERGER_TEST_FILES_PATH = os.path.join("tests", "files", "yapf")


@pytest.mark.parametrize("path", [
    "redundant_space",
])
def test_merge(path):
    default_merger_test(YapfMerger, path, YAPF_MERGER_TEST_FILES_PATH)
