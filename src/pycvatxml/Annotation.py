"""

"""
import logging
from enum import Enum
from typing import List, Tuple
import geojson as gs
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

    def getstringfields(self) -> List[str]:
        if self == Annotationtypes.UNKNOWN:
            return []
        fields = ["source"]
        return fields

    def getnumericfields(self) -> List[str]:
        if self == Annotationtypes.UNKNOWN:
            return []
        fields = ["z_order", "occluded"]
        if self == Annotationtypes.ELLIPSE:
            fields += ["cx", "cy", "rx", "ry", "rotation"]
        if self == Annotationtypes.RECTANGLE:
            return ["xtl", "ytl", "xbr", "ybr", "rotation"]
        return fields

    def haspoints(self) -> bool:
        if self in [
            Annotationtypes.POLYGON,
            Annotationtypes.POINTS,
            Annotationtypes.POLYLINE,
        ]:
            return True
        return False


class Annotation:
    def __init__(self) -> None:
        self.type = Annotationtypes.UNKNOWN  # Annotationtypes
        self.label = ""  # type:str
        self.points = []  # type:List[Tuple[float, float]]
        self.nvalues = {}  # type:dict[str, float]
        self.svalues = {}  # type:dict[str, str]
        self.attributes = []  # type:List[dict[str, str]]
        self.log = logging.getLogger("CvatXml:Annotation")  # type: logging.Logger

    def __str__(self) -> str:
        return self.label

    def fromxml(self, e: _Element) -> None:
        self.type = self.type.fromstr(e.tag)
        self.label = e.attrib.get("label", "")
        if self.type.haspoints():
            pointsstr = e.attrib.get("points", "")
            for pt in pointsstr.split(";"):
                pts = pt.split(",")
                self.points.append((float(pts[0]), float(pts[1])))
        for v in self.type.getnumericfields():
            self.nvalues[v] = float(e.attrib.get(v, "nan"))
        for v in self.type.getstringfields():
            self.svalues[v] = e.attrib.get(v, "nan")

    def as_geojson(self) -> gs.Polygon:
        if self.type == Annotationtypes.POLYGON:
            pts = self.points.copy()
            pts.append(pts[0])
            polygon = gs.Polygon([pts])
            if not polygon.is_valid:
                self.log.warning("CvatXml: 'Polygon is not valid!'")
            return polygon
        else:
            return gs.Polygon()
