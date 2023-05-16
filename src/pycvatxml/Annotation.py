"""

"""
from enum import Enum
from typing import List, Tuple

from lxml.etree import _Element


class Annotationtypes(Enum):
    RECTANGLE = 0
    POLYGON = 1
    POLYLINE = 2
    POINTS = 3
    ELLIPSE = 4
    CUBOID = 5
    MASK = 6
    TAG = 7
    UNKNOWN = -1

    def fromstr(self, s: str) -> "Annotationtypes":
        if s == "polygon":
            return Annotationtypes.POLYGON
        if s == "box":
            return Annotationtypes.RECTANGLE
        if s == "ellipse":
            return Annotationtypes.ELLIPSE
        return Annotationtypes.UNKNOWN

    def getfields(self) -> List[str]:
        if self == Annotationtypes.ELLIPSE:
            return ["cx", "cy", "rx", "ry"]
        if self in [
            Annotationtypes.POLYGON,
            Annotationtypes.POINTS,
            Annotationtypes.POLYLINE,
        ]:
            return ["points"]
        if self == Annotationtypes.RECTANGLE:
            return ["xtl", "ytl", "xbr", "ybr"]
        return [""]


class Annotation:
    def __init__(self) -> None:
        self.type = Annotationtypes.UNKNOWN  # Annotationtypes
        self.label = ""  # type:str
        self.points = []  # type:List[Tuple[float, float]]
        self.values = []  # type:List[dict[str, float]]
        self.attributes = []  # type:List[dict[str, str]]

    def __str__(self) -> str:
        return self.label

    def fromxml(self, e: _Element) -> None:
        self.type = self.type.fromstr(e.tag)
        self.label = e.attrib.get("label", "")
        if "points" in self.type.getfields():
            pointsstr = e.attrib.get("points", "")
            for pt in pointsstr.split(";"):
                pts = pt.split(",")
                self.points.append((float(pts[0]), float(pts[1])))
        else:
            for v in self.type.getfields():
                self.values.append({v: float(e.attrib.get(v, "nan"))})
