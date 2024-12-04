from __future__ import annotations
from enum import IntEnum

from jam.lib.sphere_mesh import gen_mesh, gen_voronoi

from jam.core.map_render import PlanetRenderer

class Structure:
    pass

class Sector:

    def __init__(self, id: int):
        self.id: int = id

        self.neighbors: tuple[int] = ()
        self.triangles: tuple[int] = ()

        self.controller: int = -1

        self.logisitics_level: float = 0.0
        self.logisitics_cap: float = 0.0
        self.logisitics_gain: float = 0.0
        self.logisitics_drain: float = 0.0

        self.structures: set[Structure] = set()

    def add_structure():
        pass

    def remove_structure():
        pass

class PlanetSize(IntEnum):
    TINY = 256
    SMALL = 512
    MEDIUM = 1024
    LARGE = 2048
    HUGE = 4096

class PlanetNoise(IntEnum):
    NONE = 0
    LOW = 1
    MEDIUM = 10
    HIGH = 100
NOISE_SCALE = 1000.0

class Planet:

    def __init__(self, sector_count: int, noise: PlanetNoise):
        # Mesh Data
        self.sphere, self.triangles, self.edges = gen_mesh(sector_count, noise/NOISE_SCALE)
        self.centers, self.cells = gen_voronoi(self.sphere, self.triangles, self.edges)

        # Game Play

        # GL Rendering
        self.renderer = PlanetRenderer(self.sphere, self.centers, self.cells, self.triangles, self.edges)
    
    def draw(self):
        self.renderer.render()

    def update(self):
        pass