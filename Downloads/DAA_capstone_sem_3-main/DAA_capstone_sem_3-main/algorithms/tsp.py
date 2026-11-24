def nearest_neighbor_tsp(start, destinations, distance_matrix):

    unvisited = set(destinations)

    # Starting location should not be visited again
    unvisited.discard(start)

    current = start

    route = [start]

    total_distance = 0

    # Visit nearest unvisited location
    while unvisited:

        nearest = None
        min_distance = float('inf')

        for location in destinations:

            if location in unvisited:

                distance = distance_matrix[current][location]

                if distance < min_distance:

                    min_distance = distance
                    nearest = location

        if nearest is None or min_distance == float('inf'):

            raise ValueError("Some destinations are unreachable.")

        route.append(nearest)

        total_distance += min_distance

        current = nearest

        unvisited.remove(nearest)

    # Return to warehouse
    return_distance = distance_matrix[current][start]

    if return_distance == float('inf'):

        raise ValueError("Cannot return to warehouse.")

    route.append(start)

    total_distance += return_distance

    return route, total_distance