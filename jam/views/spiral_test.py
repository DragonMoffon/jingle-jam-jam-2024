from array import array
from random import uniform
from math import pi, sin, cos, acos
from jam.core.application import View

from jam.lib.fly import FlyAroundGrip
from jam.lib.delaunator import Delaunator

import arcade
import arcade.gl as gl


from resources import load_program

def circumcenter(a, b, c):
    def diff(u, v): return u[0] - v[0], u[1] - v[1], u[2] - v[2]
    def dot(u, v): return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]
    def cross(u, v): return u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]

    ab = diff(b, a)
    ac = diff(c, a)
    n = cross(ab, ac)

    lx, ly, lz = cross(n, ab)
    rx, ry, rz = cross(ac, n)

    ab_d = dot(ab, ab)
    ac_d = dot(ac, ac)
    n_d = dot(n, n)

    vx = (lx * ac_d + rx * ab_d) / (2.0 * n_d)
    vy = (ly * ac_d + ry * ab_d) / (2.0 * n_d)
    vz = (lz * ac_d + rz * ab_d) / (2.0 * n_d)

    r = (vx*vx + vy*vy + vz*vz)**0.5

    x, y, z = a[0] + vx, a[1] + vy, a[2] + vz

    d = (x*x + y*y + z*z)**0.5

    return r, x / d, y / d, z / d

def gen_spiral(count: int = 100, jitter: float = 0.0):
    ratio = (1.0 + 5**0.5)/2.0
    for i in range(count):
        yield 2.0 * pi * i / ratio + uniform(-jitter, jitter), acos(1 - 2.0 *(i + 0.5) / count) + uniform(-jitter, jitter)

def gen_sphere(spiral: tuple[tuple[float, float]]):
    for theta, phi in spiral:
        yield cos(theta) * sin(phi), sin(theta) * sin(phi), cos(phi)

def rotate_points(target, source, points):
    # https://math.stackexchange.com/questions/180418/calculate-rotation-matrix-to-align-vector-a-to-vector-b-in-3d
    a1, a2, a3 = target
    b1, b2, b3 = source
    v1, v2, v3 = a2*b3 - a3*b2, a3*b1 - a1*b3, a1*b2 - a2*b1
    angle = a1*b1 + a2*b2 + a3*b3
    # s = (v1*v1 + v2*v2 + v3*v3)**0.5
    c = 1/(1 + angle)
    
    m11, m12, m13, m21, m22, m23, m31, m32, m33 = (
        1 - (v2*v2 + v3*v3)*c, v1*v2*c - v3, v1*v3*c + v2,
        v1*v2*c + v3, 1 - (v1*v1 + v3*v3)*c, v2*v3*c - v1,
        v1*v3*c - v2, v2*v3*c + v1, 1 - (v1*v1 + v2*v2)*c
    )

    for x, y, z in points:
        yield m11*x + m12*y + m13*z, m21*x + m22*y + m23*z, m31*x + m32*y + m33*z
 
def gen_stereo(sphere: tuple[tuple[float, float, float]]):
    for x, y, z in sphere:
        yield x / (1 - z), y / (1 - z)

def close_sphere(sphere: tuple, triangles: list[int], edges: list[int]):
    # using the triangulation of a sphere use the last point to close the convex hull
    def n(e): return e - 2 if e % 3 == 2 else e + 1
    def p(e): return e + 2 if e % 3 == 0 else e - 1

    start = edges.index(-1)

    edge = n(start)
    hull = [start]
    while True:
        while edges[edge] != -1:
            flip = edges[edge] # flip the outgoing edge
            edge = n(flip) # get the next edge of the ingoing
        if edge == start:
            break
        hull.append(edge)
        edge = n(edge)

    c = len(sphere) - 1
    root = len(edges) # This will become the idx of the first edge of the cap
    tail = root + len(hull) * 3 - 2
    for edge in hull:
        a = triangles[edge]
        b = triangles[n(edge)]
        triangles.extend((a, c, b))
        l = len(edges)
        edges[edge] = l + 2
        edges.extend((tail, len(edges)+3, edge))
        tail = l + 1
    edges[-2] = root

def voronoi(sphere, tri, edge):
    offset = len(sphere)
    centers = [circumcenter(sphere[tri[3*t]], sphere[tri[3*t+1]], sphere[tri[3*t+2]]) for t in range(0, len(tri)//3)]

    def n(e): return e - 2 if e % 3 == 2 else e + 1

    def points():
        for point in sphere:
            yield 0.0
            for p in point:
                yield p
        for point in centers:
            for p in point:
                yield p

    def indices():
        for node in range(0, len(sphere)):
            start = edge[tri.index(node)] # This gets an ingoing edge of the point
            triangles = [start]
            outgoing = n(start)
            incoming = edge[outgoing]
            while incoming != start:
                yield node
                yield offset+triangles[-1]//3
                yield offset+incoming//3
                triangles.append(incoming)
                outgoing = n(incoming)
                incoming = edge[outgoing]
            yield node
            yield offset+triangles[-1]//3
            yield offset+incoming//3
            print([i//3 for i in triangles])
    return points(), indices()

def squash(p):
    for i in p:
        for j in i:
            yield j

class SpiralView(View):

    def __init__(self) -> None:
        super().__init__()
        self.window.set_exclusive_mouse(True)
        self.window.set_mouse_visible(False)

        ctx = self.window.ctx
        self.cam = arcade.camera.PerspectiveProjector()
        self.cam.view.position = (0.0, 0.0, 100.0)
        self.cam.projection.far = 1000.0
        self.grip = FlyAroundGrip(self.cam.view)

        self.spiral = tuple(gen_spiral(1024, 0.02))[::-1]
        self.sphere = tuple(gen_sphere(self.spiral))
        self.rot = tuple(rotate_points(self.sphere[-1], (0.0, 0.0, 1.0), self.sphere))
        self.sterio = tuple(gen_stereo(self.rot[:-1]))
        d = Delaunator(tuple(squash(self.sterio)))
        self.tri, self.half = d.triangles, d.halfedges
        close_sphere(self.sphere, self.tri, self.half)
        data, indices = voronoi(self.sphere, self.tri, self.half)

        self.data = tuple(data)
        self.indices = tuple(indices)

        self.buf = gl.BufferDescription(ctx.buffer(data=array('f', self.data)), '1f 3f', ['in_circ', 'in_pos'])
        self.geo = ctx.geometry(
            [self.buf],
            index_buffer=ctx.buffer(data=array('i', self.indices)),
            index_element_size=4,
            mode=gl.TRIANGLES
        )

        # self.buf = gl.BufferDescription(ctx.buffer(data=array('f', squash(self.sphere))), '3f', ['in_pos'])
        # self.geo_tri = ctx.geometry(
        #     [self.buf],
        #     index_buffer=ctx.buffer(data=array('i', self.tri)),
        #     index_element_size=4,
        #     mode=gl.TRIANGLES
        # )
        # self.geo_points = ctx.geometry(
        #     [self.buf],
        #     mode=gl.POINTS
        # )
        self.program = load_program(ctx, vertex_shader='voronoi_vs', fragment_shader='voronoi_fs')
        self.program['radius'] = 100.0

    def on_draw(self) -> None:
        self.clear()
        with self.window.ctx.enabled(self.window.ctx.DEPTH_TEST):
            self.window.ctx.point_size = 5.0
            with self.cam.activate():
                self.geo.render(self.program)
                # self.geo_points.render(self.program)

    def on_update(self, delta_time):
        self.grip.update(delta_time)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.window.close()
            return True
        self.grip.press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.grip.release(symbol, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.grip.look(x, y, dx, dy)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.grip.zoom(scroll_y)