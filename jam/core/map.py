from __future__ import annotations

def link_nodes(a: Node, b: Node, bi: bool = True):
    a.neighbors.add(b)
    if bi:
        b.neighbors.add(a)

def unlink_nodes(a: Node, b: Node, bi: bool = True):
    a.neighbors.discard(b)
    if bi:
        b.neighbors.discard(a)

class Node:
    def __init__(self):
        self.neighbors: set[Node] = set()

class Map:
    
    def __init__(self):
        self.sectors: set[Node] = set()