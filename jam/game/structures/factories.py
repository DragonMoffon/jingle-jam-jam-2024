from jam.core.data.structure import StructureData
from jam.core.logic.structure import Structure, Anchor


class HeartFactoryData(StructureData):
    cost: float = float("inf")  # You only get one!
    capacity: float = 100.0
    base: float = 0.0
    drain: float = 0.0
    anchor = Anchor.CORE


class HeartFactory(Structure):

    def update(self, dt) -> None:
        source = self.data.sector
        sector = self.source.
