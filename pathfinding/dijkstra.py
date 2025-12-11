"""Module for Dijkstra algorithm."""

import heapq

import numpy as np


def algorithm_dijkstra(
    matrix: np.ndarray, start_vertex: int, end_vertex: int
) -> tuple[list[int], float]:
    """
    Find shortest path using Dijkstra algorithm.

    Args:
        matrix: adjacency matrix where matrix[i][j] is distance from i to j.
                np.inf means no connection.
        start_vertex: index of start vertex.
        end_vertex: index of end vertex.

    Returns:
        tuple: (list of vertex indices representing the path, total distance).
               Returns ([], np.inf) if path is not found.

    """
    n = matrix.shape[0]

    distances = np.full(n, np.inf)
    previous = np.full(n, -1, dtype=int)
    distances[start_vertex] = 0.0

    priority_queue = [(0.0, start_vertex)]

    while priority_queue:
        current_dist, u = heapq.heappop(priority_queue)

        if current_dist > distances[u]:
            continue

        if u == end_vertex:
            break

        for v in range(n):
            weight = matrix[u][v]

            if weight != np.inf and weight >= 0:
                distance = current_dist + weight

                if distance < distances[v]:
                    distances[v] = distance
                    previous[v] = u
                    heapq.heappush(priority_queue, (distance, v))

    if distances[end_vertex] == np.inf:
        return [], np.inf

    path = []
    current = end_vertex
    while current != -1:
        path.append(current)
        current = previous[current]

    return path[::-1], distances[end_vertex]


if __name__ == "__main__":
    # Test block
    inf = np.inf
    test_matrix = np.array([
        [inf, 1.0, inf, 3.0, inf],  # 0
        [1.0, inf, 4.0, inf, 1.0],  # 1
        [inf, 4.0, inf, inf, inf],  # 2
        [3.0, inf, inf, inf, 1.0],  # 3
        [inf, 1.0, inf, 1.0, inf],  # 4
    ])

    test_path, test_dist = algorithm_dijkstra(test_matrix, 0, 4)
    print(f"Path: {test_path}, Length: {test_dist}")  # noqa: T201

    assert test_path == [0, 1, 4]  # noqa: S101
    assert test_dist == 2.0  # noqa: S101, PLR2004
    print("Test passed!")  # noqa: T201
