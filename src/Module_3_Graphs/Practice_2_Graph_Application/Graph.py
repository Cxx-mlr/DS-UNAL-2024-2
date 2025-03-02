from typing_extensions import List, Tuple, Set, Unpack, TypeAlias, TypeVar, Optional
from pathlib import Path
import itertools
import sys
import csv

from rich.table import Table

from utils import console

T = TypeVar("T")
Node: TypeAlias = str
Edge: TypeAlias = Tuple[str, str, Unpack[Tuple[int, ...]]]
Matrix: TypeAlias = List[List[T]]


class Graph:
    def __init__(self, filename: Optional[str] = None):
        self._filename = filename

        if self._filename is None:
            return

        self.load_data()

    @property
    def _representative(self) -> Matrix[int]:
        return self._adj_matrices[0]

    def _ensure_node(self, node: str) -> Optional[int]:
        if (idx := self._node_index.get(node)) is None:
            console.print(f"[red]No se encontró el nodo {node!r}[/]")
        return idx

    def load_data(self, filename: Optional[str] = None) -> None:
        filename = filename or self._filename

        if filename is None:
            raise ValueError("Filename must be provided")

        road_data_path = Path(__file__).parent / "data" / filename
        with open(road_data_path, "rt", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            self.nodes: Set[Node] = set()
            self.edges: List[Edge] = list()

            for line_count, row in enumerate(csv_reader):
                if line_count == 0:
                    self._header = row
                    self._weights_length = len(self._header) - 2
                    continue

                node_x, node_y, *weights = row

                self.nodes.add(node_x)
                self.nodes.add(node_y)

                self.edges.append((node_x, node_y, *map(int, weights)))

        self._node_index = {node: idx for idx, node in enumerate(self.nodes)}
        self._index_node = {idx: node for node, idx in self._node_index.items()}
        self._build_adj_matrices()
        self._floyd_warshall()

    def _build_adj_matrices(self) -> None:
        self._adj_matrices: List[Matrix[T]] = [
            [[0] * len(self.nodes) for _ in range(len(self.nodes))]
            for _ in range(self._weights_length)
        ]

        for node_x, node_y, *weights in self.edges:
            i, j = self._node_index[node_x], self._node_index[node_y]
            for weight_index, adj_matrix in enumerate(self._adj_matrices):
                adj_matrix[i][j] = weights[weight_index]
                adj_matrix[j][i] = weights[weight_index]

    def _floyd_warshall(self) -> None:
        self._shortest_path_matrices: List[Matrix[int]] = []
        self._next_hop_matrices: List[Matrix[int]] = []

        for matrix in self._adj_matrices:
            n = len(matrix)
            shortest_path = [[sys.maxsize] * n for _ in range(n)]
            next_hop = [[-1] * n for _ in range(n)]

            for i, j in itertools.product(*itertools.tee(range(n))):
                if i == j:
                    shortest_path[i][j] = 0
                elif matrix[i][j] != 0:
                    shortest_path[i][j] = matrix[i][j]
                    next_hop[i][j] = j

            for k, i, j in itertools.product(*itertools.tee(range(n), 3)):
                if (
                    shortest_path[i][k] != sys.maxsize
                    and shortest_path[k][j] != sys.maxsize
                    and shortest_path[i][j] > shortest_path[i][k] + shortest_path[k][j]
                ):
                    shortest_path[i][j] = shortest_path[i][k] + shortest_path[k][j]
                    next_hop[i][j] = next_hop[i][k]

            self._shortest_path_matrices.append(shortest_path)
            self._next_hop_matrices.append(next_hop)

    def _is_adjacent(self, node_x: int, node_y: int) -> bool:
        return self._representative[node_x][node_y] != 0

    def _graph_density(self) -> str:
        n = len(self._representative)
        edge_count = sum(
            1 for i in range(n) for j in range(n) if self._representative[i][j] != 0
        )
        max_edges = n * (n - 1) / 2
        density = edge_count / max_edges

        return "disperso" if density < 0.5 else "denso"

    def shortest_path(self, start_node: str, end_node: str) -> None:
        start_idx = self._ensure_node(start_node)
        end_idx = self._ensure_node(end_node)

        if start_idx is None or end_idx is None:
            console.print(f"[red]No hay ruta entre {start_node} y {end_node}.[/]")
            return

        for weight_index, (shortest_path, next_hop) in enumerate(
            zip(self._shortest_path_matrices, self._next_hop_matrices), start=2
        ):
            weight_header = self._header[weight_index]
            console.print(
                f"- Distancia más corta de {start_node!r} a {end_node!r}"
                f" : {shortest_path[start_idx][end_idx]}"
                + (f" {weight_header}" if weight_header else "")
            )
            print(end="\t")

            path = []
            current = start_idx
            while current != end_idx:
                path.append(self._index_node[current])
                current = next_hop[current][end_idx]
            path.append(end_node)

            console.print("[yellow]" + " -> ".join(path))

            if weight_index - 1 < self._weights_length:
                print()

    def check_adjacency(self, start_node: str, end_node: str):
        start_idx = self._ensure_node(start_node)
        end_idx = self._ensure_node(end_node)

        if start_idx is None or end_idx is None:
            console.print(f"[red]No hay ruta entre {start_node} y {end_node}.[/]")
            return

        adjacent = self._is_adjacent(start_idx, end_idx)
        console.print(
            f"\nLos nodos [blue]{start_node!r}[/] y [blue]{end_node!r}[/] {'son' if adjacent else 'no son'} adyacentes."
        )

    def display_info(self):
        table = Table(title="[green]Información del Grafo")

        table.add_column("Propiedad", justify="right", style="cyan", no_wrap=True)
        table.add_column("Valor", style="magenta")

        table.add_row("Nodos", str(len(self.nodes)))
        table.add_row("Aristas", str(len(self.edges)))
        table.add_row("Densidad", self._graph_density())

        table.add_row("Complejidad Floyd-Warshall", "O(n^3)")
        table.add_row("Espacio Auxiliar Floyd-Warshall", "O(n^2)")

        print()
        console.print(table)
        print()
