from jam.core.data.structure import StructureData, Anchor
from jam.core.logic.structure import Structure


class SpreaderPylonData(StructureData):
    cost: float = 5.0
    capacity: float = 25.0
    base: float = 0.0
    drain: float = 0.0
    anchor = Anchor.CORE


class SpreaderPylon(Structure):

    def update(self, dt) -> None:
        pass


class LinkedPylonData(StructureData):
    cost = 5.0
    capacity = 25.0
    base = 0.0
    drain = 0.0
    anchor = Anchor.CORE


class LinkedPylon(Structure):

    def update(self, dt) -> None:
        pass
