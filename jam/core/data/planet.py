from __future__ import annotations
from array import array
from enum import IntEnum

from jam.lib.sphere_mesh import gen_mesh, gen_voronoi


class PlanetSize(IntEnum):
    TINY = 256
    SMALL = 512
    MEDIUM = 1024
    LARGE = 2048
    HUGE = 4096


class PlanetNoise(IntEnum):
    NONE = 0
    LOW = 5
    MEDIUM = 15
    HIGH = 20


NOISE_SCALE = 1000.0


class PlanetData:

    def __init__(self, sector_count: int, noise: PlanetNoise):
        # Mesh Data
        self.size = sector_count
        self.noise = noise
        self.sphere, self.triangles, self.edges = gen_mesh(
            sector_count, noise / NOISE_SCALE
        )
        self.neighbors: list = [[] for _ in range(self.size)]
        for idx, point in enumerate(self.triangles):
            self.neighbors[point].append(self.triangles[self.edges[idx]])
        self.centers, self.cells, self.roots = gen_voronoi(
            self.sphere, self.triangles, self.edges
        )

        # Game Play

        # Packed array of sector data. We don't care who owns a sector for some interesting politics
        # amount, cap, gain
        self.source = array("f", (0,) * 3 * sector_count)
        self.target = array("f", (0,) * 3 * sector_count)
        self.stale_data = False

    def grow_sector(self, sector: int, value: float) -> None:
        self.target[sector * 3] += value

    def flip_logistics(self) -> None:
        self.source, self.target = self.target, self.source
        # reset change
        for idx in range(self.size):
            v, c = self.source[3 * idx], self.source[3 * idx + 1]
            self.source[3 * idx] = max(0.0, min(c, v))  # clamp to capacity
            self.target[3 * idx + 2] = 0.0
        self.stale_data = True
