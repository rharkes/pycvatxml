import pytest as pytest
from pathlib import Path
from pycvatxml import CvatXml


@pytest.fixture
def files():
    root = Path(
        Path.cwd(),
        "tests",
        "testdata",
    )
    return [
        Path(root, "annotations.xml"),
        Path(root, "testset.zip"),
    ]


def testloading(files):
    cvx = CvatXml()
    for file in files:
        cvx.load(file)
        assert cvx.valid
