"""

"""
from pathlib import Path
from typing import Union, Any, IO
import os
import logging
from uuid import uuid4
from zipfile import ZipFile
import geojson as gs
from lxml import etree
from lxml.etree import _Element

from pycvatxml.Image import Image
from pycvatxml.MetaData import MetaData


class CvatXml:
    """ """

    def __init__(self) -> None:
        self.tree = etree.Element("root")  # type:_Element
        self.valid = False  # type: bool
        self.log = logging.getLogger("CvatXml")
        self.version = ""  # type: str
        self.meta = MetaData()  # type:MetaData
        self.images = []  # type:list[Image]

    def __bool__(self) -> bool:
        return self.valid

    def load(self, pth: Union[str, os.PathLike[Any]]) -> None:
        pth = Path(pth)
        if not pth.exists() or not pth.is_file():
            raise FileNotFoundError(pth)
        if pth.suffix == ".zip":
            with ZipFile(pth, "r") as myzip:
                with myzip.open("annotations.xml") as myfile:
                    self._loadxmlstream(myfile)
            return
        if pth.suffix == ".xml":
            with open(pth, "rb") as myfile:
                self._loadxmlstream(myfile)
        else:
            self.log.error(f"Invalid extension {pth.suffix}")
        self.valid = True

    def _loadxmlstream(self, stream: IO[bytes]) -> None:
        self.tree = etree.parse(stream)
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
                self.meta.fromxml(e)
            elif e.tag == "image":
                im = Image()
                im.fromxml(e)
                self.images.append(im)
            else:
                self.log.warning(f"Unkown tag: {e.tag}")

    def as_geojson(self, imageid: int = 0) -> gs.FeatureCollection:
        features = []
        for layer in self.meta.labels:
            props = {
                "objectType": "annotation",
                "name": layer.name,
                "classification": {
                    "name": layer.name,
                    "color": layer.color.getrgb(),
                },
                "isLocked": False,
            }
            for annotation in self.images[imageid].annotations:
                if annotation.label == layer.name:
                    geometry = annotation.as_geojson()
                    if len(geometry["coordinates"]) == 0:
                        continue
                    features.append(
                        gs.Feature(geometry=geometry, properties=props, id=str(uuid4()))
                    )
        return gs.FeatureCollection(features)

    def to_geojson(self, pth: Union[str, os.PathLike[Any]]) -> None:
        """
        Save regions as geojson. This file can be loaded in QuPath.

        :param pth: Location to save the .geojson to.
        """
        pth = Path(pth)
        if not pth.suffix:
            pth = Path(pth.parent, pth.name + ".geojson")
        with open(pth, "wt") as f:
            f.write(gs.dumps(self.as_geojson(), sort_keys=True))
