import pytest as pytest
from pathlib import Path
from pycvatxml import CvatXml


@pytest.fixture
def files():
    return [
        Path(
            Path.cwd(),
            "tests",
            "testdata",
            "annotations.xml",
        ),
    ]


def testloading(files):
    cvx = CvatXml()
    for file in files:
        cvx.load(file)
