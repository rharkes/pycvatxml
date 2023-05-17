"""

"""
from lxml.etree import _Element
import geojson as gs

from pycvatxml.MetaData import MetaData
from pycvatxml.Annotation import Annotation


class Image:
    def __init__(self) -> None:
        self.id = -1  # type:int
        self.name = ""  # type:str
        self.width = -1  # type:int
        self.height = -1  # type:int
        self.annotations = []  # type:list[Annotation]

    def __str__(self) -> str:
        return self.name

    def fromxml(self, e: _Element) -> None:
        self.id = int(e.attrib.get("id", -1))
        self.width = int(e.attrib.get("width", -1))
        self.height = int(e.attrib.get("height", -1))
        self.name = e.attrib.get("name", "")
        for ch in e.getchildren():
            a = Annotation()
            a.fromxml(ch)
            self.annotations.append(a)
