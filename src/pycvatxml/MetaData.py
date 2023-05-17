import logging
from typing import List

from lxml.etree import _Element


class Attribute:
    def __init__(self) -> None:
        self.name = ""
        self.mutable = False
        self.input_type = ""
        self.default_value = ""
        self.values = []  # type: List[str]

    def __str__(self) -> str:
        return self.name

    def fromxml(self, e: _Element) -> None:
        for ch in e.getchildren():
            if ch.tag == "name":
                self.name = ch.text
            if ch.tag == "mutable":
                self.mutable = ch.text == "True"
            if ch.tag == "input_type":
                self.input_type = ch.text
            if ch.tag == "default_value":
                self.default_value = ch.text
            if ch.tag == "values":
                self.values = ch.text.split("\n")


class Label:
    def __init__(self) -> None:
        self.name = ""
        self.color = Color()
        self.mytype = ""
        self.attributes = []  # type: List[Attribute]

    def __str__(self) -> str:
        return self.name

    def fromxml(self, e: _Element) -> None:
        for ch in e.getchildren():
            if ch.tag == "name":
                self.name = ch.text
            if ch.tag == "color":
                self.color.sethexcolor(ch.text)
            if ch.tag == "mytype":
                self.mytype = ch.text
            if ch.tag == "attributes":
                for attribute in ch.getchildren():
                    myatt = Attribute()
                    myatt.fromxml(attribute)
                    self.attributes.append(myatt)


class MetaData:
    """ """

    def __init__(self) -> None:
        self.labels = []  # type: List[Label]

    def fromxml(self, e: _Element) -> None:
        labels = self.getlabels(e)
        for label in labels:
            mylabel = Label()
            mylabel.fromxml(label)
            self.labels.append(mylabel)

    def getlabels(self, e: _Element) -> _Element:
        for ch in e.getchildren():
            if ch.tag == "job":
                for ch2 in ch.getchildren():
                    if ch2.tag == "labels":
                        return ch2


class Color:
    """
    Class for keeping color rgb information
    """

    def __init__(self) -> None:
        self.rgb = (0).to_bytes(length=3, byteorder="little")  # type:bytes
        self.log = logging.getLogger("CvatXml-Color")

    def __str__(self) -> str:
        return hex(int.from_bytes(self.rgb, byteorder="little"))

    def getrgb(self) -> tuple[int, int, int]:
        return int(self.rgb[0]), int(self.rgb[1]), int(self.rgb[2])

    def setrgb(self, r: int, g: int, b: int) -> None:
        if all([x <= 255 for x in [r, g, b]]):
            self.rgb = (r + g * 2**8 + b * 2**16).to_bytes(
                length=3, byteorder="little"
            )
            return
        self.log.error("Color should be <255 for each color")

    def getlinecolor(self) -> str:
        return str(int.from_bytes(self.rgb, byteorder="little"))

    def setlinecolor(self, color: str) -> None:
        self.rgb = int(color).to_bytes(length=3, byteorder="little")

    def sethexcolor(self, color: str) -> None:
        color = color.lstrip("#")
        colorrgb = tuple(int(color[i : i + 2], 16) for i in (4, 2, 0))
        self.setrgb(*colorrgb)
