from jam.core.data import SessionData


class Structure:

    def __init__(self, idx: int, source: SessionData):
        self.idx = idx
        self.data = source.structues[idx]
        self.source = source

    def update(self, dt) -> None:
        pass

    def clicked(self) -> None:
        pass

    def destroyed(self) -> None:
        pass
