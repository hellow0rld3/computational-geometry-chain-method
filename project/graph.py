from typing import List, Optional, Dict
from functools import cmp_to_key

class Vertex:
    """Reprezentuje wierzchołek w podziale poligonowym."""
    def __init__(self, id: int, x: float, y: float):
        self.id = id
        self.x = x
        self.y = y
        self.in_edges: List['Edge'] = []
        self.out_edges: List['Edge'] = []

    def __repr__(self):
        return f"V{self.id}({self.x}, {self.y})"

    def __lt__(self, other: 'Vertex'):
        """Porządek y-monotoniczny (dół -> góra)."""
        if self.y != other.y:
            return self.y < other.y
        return self.x < other.x


class Edge:
    """Reprezentuje skierowaną krawędź (zawsze w górę)."""
    def __init__(self, start: Vertex, end: Vertex):
        # Automatyczne zapewnienie, że start jest "niżej" niż end
        if end < start:
            self.start, self.end = end, start
        else:
            self.start, self.end = start, end
            
        self.weight = 0
        self.chains: List[int] = []

        self.start.out_edges.append(self)
        self.end.in_edges.append(self)

    def __repr__(self):
        return f"Edge({self.start.id} -> {self.end.id}, w={self.weight})"


class Graph:
    """Struktura przechowująca graf."""
    def __init__(self):
        self.vertices: Dict[int, Vertex] = {}
        self.edges: List[Edge] = []
        self._next_id = 0

    def add_vertex(self, x: float, y: float) -> Vertex:
        v = Vertex(self._next_id, x, y)
        self.vertices[self._next_id] = v
        self._next_id += 1
        return v

    def add_edge(self, v1_id: int, v2_id: int) -> Optional[Edge]:
        v1, v2 = self.vertices.get(v1_id), self.vertices.get(v2_id)
        if v1 is not None and v2 is not None:
            e = Edge(v1, v2)
            self.edges.append(e)
            return e
        return None

    @staticmethod
    def _get_orientation(v: Vertex, e1: Edge, e2: Edge) -> float:
        """
        Oblicza wyznacznik macierzy 2x2 (iloczyn wektorowy) dla dwóch krawędzi.
        Zwraca:
        > 0 : e2 jest na lewo od e1
        < 0 : e2 jest na prawo od e1
        = 0 : krawędzie są współliniowe
        """
       
        # Dla out_edges: v jest punktem startowym
        # Dla in_edges: v jest punktem końcowym (używamy wektorów "odwróconych")
        
        
        if e1.start == v: # out_edges
            v1_x, v1_y = e1.end.x - v.x, e1.end.y - v.y
            v2_x, v2_y = e2.end.x - v.x, e2.end.y - v.y
        else: # in_edges
            v1_x, v1_y = e1.start.x - v.x, e1.start.y - v.y
            v2_x, v2_y = e2.start.x - v.x, e2.start.y - v.y
            
        return v1_x * v2_y - v1_y * v2_x

    def get_sorted_out_edges(self, v: Vertex) -> List[Edge]:
        """Sortuje krawędzie wychodzące od prawej do lewej (lub odwrotnie)."""
        def compare(e1, e2):
            det = self._get_orientation(v, e1, e2)
            if det > 0: return 1  # e2 jest bardziej "na lewo" niż e1
            if det < 0: return -1 # e2 jest bardziej "na prawo" niż e1
            return 0
        
        return sorted(v.out_edges, key=cmp_to_key(compare))

    def get_sorted_in_edges(self, v: Vertex) -> List[Edge]:
        """Sortuje krawędzie wchodzące angularnie."""
        def compare(e1, e2):
            det = self._get_orientation(v, e1, e2)
            # Logika dla krawędzi wchodzących 
            if det > 0: return -1
            if det < 0: return 1
            return 0
            
        return sorted(v.in_edges, key=cmp_to_key(compare))

    def get_sorted_vertices(self) -> List[Vertex]:
        return sorted(self.vertices.values())