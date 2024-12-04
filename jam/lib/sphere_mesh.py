from random import uniform
from math import cos, sin, acos, pi

from jam.lib.delaunator import Delaunator

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
        yield x / (1 - z)
        yield y / (1 - z)

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

def gen_mesh(size: int, noise: float = 0.0) -> tuple[tuple[tuple[float, float, float], ...], list[int], list[int]]:
    spiral = tuple(gen_spiral(size, noise))[::-1] # We reverse it so the south pole is last
    sphere = tuple(gen_sphere(spiral))
    projection = tuple(gen_stereo(rotate_points(sphere[-1], (0.0, 0.0, 1.0), sphere[:-1])))
    triangulation = Delaunator(projection)
    triangles, edges = triangulation.triangles, triangulation.halfedges
    close_sphere(sphere, triangles, edges)
    
    return sphere, triangles, edges

def gen_voronoi(sphere: tuple[tuple[float, float, float], ...], triangles: tuple[int, ...], edges: tuple[int, ...]):
    def n(e): return e - 2 if e % 3 == 2 else e + 1
    def cell(point: int):
        # the index of the point is for an outgoing edge, we need it's mirror to get the ingoing edge
        start = edges[triangles.index(point)]
        cell_points = [start//3]
        outgoing = n(start)
        incoming = edges[outgoing]
        while incoming != start:
            cell_points.append(incoming//3)
            outgoing = n(incoming)
            incoming = edges[outgoing]

        return cell_points
    
    
    # The circumcenters have the same indexing as the triangles. This makes it very easy to construct them from the mesh
    centers = tuple(circumcenter(sphere[triangles[3*t]], sphere[triangles[3*t+1]], sphere[triangles[3*t+2]]) for t in range(0, len(triangles)//3))
    cells = tuple(cell(idx) for idx in range(len(sphere)))

    return centers, cells


