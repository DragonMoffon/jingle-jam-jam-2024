from enum import Enum, auto


class Anchor(Enum):
    CORNER = auto()
    OUTER = auto()
    INNER = auto()
    CORE = auto()
    TRIANGLE = auto()


class StructureData:
    cost: float = 0.0
    capacity: float = 0.0
    base: float = 0.0
    drain: float = 0.0
    anchor: Anchor = Anchor.TRIANGLE

    def __init__(self, sector: int, idx: int, position: tuple[float, float, float]):
        self.sector = sector
        self.idx = idx
        self.position = position

        self.online: bool = False
        self.integeridy: float = 1.0
