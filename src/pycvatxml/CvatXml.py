"""

"""
from pathlib import Path
from typing import Union, Any
import os
import logging

from lxml import etree
from lxml.etree import _Element

from pycvatxml.Image import Image


class CvatXml:
    """ """

    def __init__(self) -> None:
        self.tree = etree.Element("root")  # type:_Element
        self.valid = False  # type: bool
        self.log = logging.getLogger("CvatXml")
        self.version = ""  # type: str
        self.meta = etree.Element("root")  # type:_Element
        self.images = []  # type:list[Image]

    def __bool__(self) -> bool:
        return self.valid

    def load(self, pth: Union[str, os.PathLike[Any]]) -> None:
        pth = Path(pth)
        if not pth.exists() or not pth.is_file():
            raise FileNotFoundError(pth)
        if pth.suffix == "zip":
            self.log.error("sorry, no zip yet")
            return
        if pth.suffix == ".xml":
            self._loadxml(pth)
        else:
            self.log.error(f"Invalid extension {pth.suffix}")

    def _loadxml(self, pth: Union[str, os.PathLike[Any]]) -> None:
        self.tree = etree.parse(pth)
        root = self.tree.getroot()
        if root.tag != "annotations":
            self.log.error(f"Root tag is '{root.tag}'. Not a valid annotation file.")
            return
        self._getvmi(root.getchildren())
        if self.version != "1.1":
            self.log.warning(f"Version {self.version} is not officially supported.")

    def _getvmi(self, vmi: list[_Element]) -> None:
        for e in vmi:
            if e.tag == "version":
                self.version = e.text
            elif e.tag == "meta":
                self.meta = e
            elif e.tag == "image":
                im = Image()
                im.fromxml(e)
                self.images.append(im)
            else:
                self.log.warning(f"Unkown tag: {e.tag}")
