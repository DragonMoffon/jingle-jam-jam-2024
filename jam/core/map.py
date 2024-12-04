from __future__ import annotations
from array import array
from enum import IntEnum
from random import choice, random

from jam.lib.sphere_mesh import gen_mesh, gen_voronoi

from jam.core.map_render import PlanetRenderer

class Structure:
    
    def __init__(self, p, c, f, l):
        self.production: float = p
        self.capacity: float = c
        self.function: callable[[float], float] = f
        self.location: int = l

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

class Planet:

    def __init__(self, sector_count: int, noise: PlanetNoise):
        # Mesh Data
        self.size = sector_count
        self.noise = noise
        self.sphere, self.triangles, self.edges = gen_mesh(sector_count, noise/NOISE_SCALE)
        self.centers, self.cells, self.root = gen_voronoi(self.sphere, self.triangles, self.edges)

        # Game Play

        # Packed array of sector data. We don't care who owns a sector for some interesting politics
        # amount, cap, gain, loss
        self.logistics = array('f', (0,)*4*sector_count)
        self.stale_data = False
        self.structures_map: list[list[Structure]] = [[] for _ in range(sector_count)]
        self.structures: list[Structure] = []

        # GL Rendering
        self.renderer = PlanetRenderer(self.sphere, self.centers, self.cells, self.triangles, self.edges)
    
    def get_sector(self, id: int):
        a = self.logistics
        return a[4*id], a[4*id+1], a[4*id+2], a[4*id+3]
    
    def set_sector(self, id: int, v = None, c = None, g = None, d = None):
        a = self.logistics
        if v is not None:
            self.stale_data = True
            a[4*id] = v
        if c is not None:
            self.stale_data = True
            a[4*id+1] = c
        if g is not None:
            self.stale_data = True
            a[4*id+2] = g
        if d is not None:
            self.stale_data = True
            a[4*id+3] = d

    def update(self, dt):
        pass

    def fixed_update(self, dt):
        a = self.logistics
        for idx in range(0, 4*self.size):
            a[idx] = random()
        self.stale_data = True
    
    def write_sector(self):
        self.renderer.sector_map.write(data=self.logistics)
        self.stale_data = False

    def draw(self):
        if self.stale_data:
            self.write_sector()
        self.renderer.render()
