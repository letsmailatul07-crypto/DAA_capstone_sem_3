import heapq


def build_graph(locations, edges):

    graph = {location: [] for location in locations}

    for u, v, weight in edges:

        # Undirected graph

        graph[u].append((v, weight))
        graph[v].append((u, weight))

    return graph


def dijkstra(graph, source):

    # Initialize distances

    dist = {
        vertex: float('inf')
        for vertex in graph
    }

    parent = {
        vertex: None
        for vertex in graph
    }

    dist[source] = 0

    # Priority queue

    pq = [(0, source)]

    while pq:

        current_dist, u = heapq.heappop(pq)

        # Ignore outdated entries

        if current_dist > dist[u]:
            continue

        # Visit neighboring vertices

        for v, weight in graph[u]:

            new_dist = current_dist + weight

            if new_dist < dist[v]:

                dist[v] = new_dist

                parent[v] = u

                heapq.heappush(
                    pq,
                    (new_dist, v)
                )

    return dist, parent


def reconstruct_path(parent, source, destination):

    path = []

    current = destination

    while current is not None:

        path.append(current)

        current = parent[current]

    path.reverse()

    if not path or path[0] != source:
        return []

    return path