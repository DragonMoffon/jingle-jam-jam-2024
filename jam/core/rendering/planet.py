from array import array

from arcade import get_window
import arcade.gl as gl

from resources import load_program

from jam.core.data.planet import PlanetData


def merge_points(points, centers):
    for point in points:
        yield 0.0
        yield point[0]
        yield point[1]
        yield point[2]

    for center in centers:
        yield center[0]
        yield center[1]
        yield center[2]
        yield center[3]


def generate_cell_indices(count, cells):
    for node in range(0, count):
        cell = cells[node][:]
        for idx, center in enumerate(cell):
            prev = cell[idx - 1]  # Thanks list wrapping
            yield center + count
            yield prev + count
            yield node


class PlanetRenderer:

    def __init__(self, planet: PlanetData):
        self.planet = planet
        self.points = planet.points
        self.centers = planet.centers
        self.cells = planet.cells
        self.triangles = planet.triangles
        self.edges = planet.edges

        self.ctx = ctx = get_window().ctx

        self.point_buffer = ctx.buffer(
            data=array("f", merge_points(self.points, self.centers))
        )
        self.point_description = gl.BufferDescription(
            self.point_buffer, "1f 3f", ["in_dist", "in_pos"]
        )

        self.mesh_indices = ctx.buffer(data=array("i", self.triangles))
        self.cell_indices = ctx.buffer(
            data=array("i", generate_cell_indices(len(self.planet.size), self.cells))
        )

        self.mesh_vbo = ctx.geometry(
            [self.point_description], self.mesh_indices, gl.TRIANGLES
        )
        self.cell_vbo = ctx.geometry(
            [self.point_description], self.cell_indices, gl.TRIANGLES
        )

        self.mesh_program = load_program(
            ctx, vertex_shader="point_vs", fragment_shader="point_fs"
        )
        self.mesh_program["radius"] = 100.0

        self.cell_program = load_program(
            ctx, vertex_shader="voronoi_vs", fragment_shader="voronoi_fs"
        )
        self.cell_program["radius"] = 100.0
        self.cell_program["edge_width"] = 0.2
        self.cell_program["core_radius"] = 4.0

        self.sector_map: gl.Texture2D = ctx.texture(
            (3, self.planet.size),
            components=1,
            dtype="f4",
            wrap_x=gl.CLAMP_TO_EDGE,
            wrap_y=gl.CLAMP_TO_EDGE,
            filter=(gl.NEAREST, gl.NEAREST),
        )

        self.render_mesh: bool = False

    def render(self) -> None:
        with self.ctx.enabled(self.ctx.CULL_FACE):
            if self.render_mesh:
                self.mesh_vbo.render(self.mesh_program)
            else:
                self.sector_map.use()
                self.cell_vbo.render(self.cell_program)
