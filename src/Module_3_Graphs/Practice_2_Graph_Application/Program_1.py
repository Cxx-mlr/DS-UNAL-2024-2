from typing_extensions import List, Tuple, Set, Iterable, Unpack, TypeAlias, TypeVar
from pathlib import Path
import sys
import csv
from rich.console import Console
from rich.table import Table
import itertools

T = TypeVar("T")
Matrix: TypeAlias = List[List[T]]


def floyd_warshall(matrix: Matrix[int]) -> Tuple[Matrix[int], Matrix[int]]:
    n = len(matrix)
    dist = [[sys.maxsize] * n for _ in range(n)]
    next_node = [[-1] * n for _ in range(n)]

    for i, j in itertools.product(*itertools.tee(range(n))):
        if i == j:
            dist[i][j] = 0
        elif matrix[i][j] != 0:
            dist[i][j] = matrix[i][j]
            next_node[i][j] = j

    for k, i, j in itertools.product(*itertools.tee(range(n), 3)):
        if (
            dist[i][k] != sys.maxsize
            and dist[k][j] != sys.maxsize
            and dist[i][j] > dist[i][k] + dist[k][j]
        ):
            dist[i][j] = dist[i][k] + dist[k][j]
            next_node[i][j] = next_node[i][k]

    return dist, next_node

def load_data(filename: str) -> Tuple[Set[str], Tuple[str, str, Unpack[Tuple[int, ...]]]]:
    road_data_path = Path(__file__).parent / "data" / filename
    with open(road_data_path, "rt", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")

        nodes = set()
        edges = []

        for line_count, row in enumerate(csv_reader):
            if line_count == 0:
                continue

            node_x, node_y, km, minutes = row

            nodes.add(node_x)
            nodes.add(node_y)

            edges.append((node_x, node_y, int(km), int(minutes)))

    return nodes, edges

def build_adj_matrices(
    nodes: Iterable[str], edges: Tuple[str, str, Unpack[Tuple[int, ...]]]
) -> List[
    Matrix[T]
]:
    node_list = list(nodes)
    node_index = {node: idx for idx, node in enumerate(node_list)}
    n = len(node_list)
    weights_size = len(edges[0]) - 2 if edges else 1

    adj_matrices = [
        [[0] * n for _ in range(n)] for _ in range(weights_size)
    ]

    for node_x, node_y, *weights in edges:
        i, j = node_index[node_x], node_index[node_y]
        for weight_index, adj_matrix in enumerate(adj_matrices):
            adj_matrix[i][j] = weights[weight_index]
            adj_matrix[j][i] = weights[weight_index]

    return adj_matrices


def is_adjacent(matrix: Matrix[T], node_x: int, node_y: int) -> bool:
    return matrix[node_x][node_y] != 0


def graph_density(matrix: Matrix[int]) -> str:
    n = len(matrix)
    edge_count = sum(1 for i in range(n) for j in range(n) if matrix[i][j] != 0)
    max_edges = n * (n - 1) / 2
    density = edge_count / max_edges

    return "disperso" if density < 0.5 else "denso"

def main():
    cities, edges = load_data("road-data.csv")
    adj_matrix_km, adj_matrix_minutes = build_adj_matrices(nodes=cities, edges=edges)

    density = graph_density(adj_matrix_km)
    num_nodes = len(cities)
    num_edges = len(edges)

    table = Table(title="Información del Grafo")

    table.add_column("Propiedad", justify="right", style="cyan", no_wrap=True)
    table.add_column("Valor", style="magenta")

    table.add_row("Nodos", str(num_nodes))
    table.add_row("Aristas", str(num_edges))
    table.add_row("Densidad", density)

    table.add_row("Complejidad Floyd-Warshall", "O(n^3)")
    table.add_row("Complejidad Floyd-Warshall (nodos)", f"O({num_nodes}^3) = {num_nodes ** 3}")
    table.add_row("Espacio Auxiliar Floyd-Warshall", "O(n^2)")
    table.add_row("Espacio Auxiliar Floyd-Warshall (nodos)", f"O({num_nodes}^2) = {num_nodes ** 2}")

    console = Console()
    console.print(table)

    shortest_paths_km = floyd_warshall(adj_matrix_km)
    shortest_paths_minutes = floyd_warshall(adj_matrix_minutes)

    city_index = {city: idx for idx, city in enumerate(cities)}

    def ensure_city(city: str) -> int:
        if (idx := city_index.get(city)) is None:
            console.print(f"[red]No se encontró la ciudad {city!r}[/]")
        return idx

    def shortest_path(start_city: str, end_city: str):
        if (start_idx := city_index.get(start_city)) is None:
            print(f"No se encontró la ciudad {start_city!r}")
            return

        if (end_idx := city_index.get(end_city)) is None:
            print(f"No se encontró la ciudad {end_city!r}")
            return

        print(
            f"Distancia más corta de {start_city!r} a {end_city!r}"
            f" : {shortest_paths_km[start_idx][end_idx]} km"
        )
        print(
            f"Distancia más corta de {start_city!r} a {end_city!r}"
            f" : {shortest_paths_minutes[start_idx][end_idx]} minutos"
        )

    shortest_path("Bogota", "Valledupar")


if __name__ == "__main__":
    main()
