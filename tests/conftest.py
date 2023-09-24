import pytest  # noqa
from pathlib import Path
import os


@pytest.fixture
def testdir_location(request):
    return Path(request.fspath).resolve().parents[1]


@pytest.fixture
def test_netrc_path(testdir_location):
    return testdir_location / ".netrc"


@pytest.fixture
def test_netrc_path_nonexisent(testdir_location):
    netrc_path = testdir_location / ".netrc-nonexisent"

    yield netrc_path

    if os.path.exists(netrc_path):
        os.remove(netrc_path)
