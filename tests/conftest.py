import pytest  # noqa
from pathlib import Path
import os


@pytest.fixture
def testdir_location(request):
    return Path(request.fspath).resolve().parents[1]


@pytest.fixture
def test_netrc_path(testdir_location):
    netrc_path = testdir_location / ".netrc"
    old_content = open(netrc_path, "r").read()

    yield netrc_path

    open(netrc_path, "w").write(old_content)


@pytest.fixture
def test_netrc_path_nonexisent(testdir_location):
    netrc_path = testdir_location / ".netrc-nonexisent"

    yield netrc_path

    if os.path.exists(netrc_path):
        os.remove(netrc_path)
