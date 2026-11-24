import time
import random
import csv
import os

from algorithms.merge_sort import merge_sort
from algorithms.knapsack import knapsack

from algorithms.dijkstra import (
    build_graph,
    dijkstra
)

from algorithms.tsp import nearest_neighbor_tsp


# Generate random parcel dataset

def generate_parcels(n):

    parcels = []

    for i in range(n):

        parcels.append({
            "id": f"P{i+1}",
            "weight": random.randint(1, 10),
            "value": random.randint(10, 100),
            "priority": random.randint(1, 3),
            "deadline": f"{random.randint(8, 18):02d}:00",
            "destination": f"L{i+1}"
        })

    return parcels


# Generate connected graph

def generate_graph(n):

    locations = ["W"] + [
        f"L{i}" for i in range(1, n)
    ]

    edges = []

    # Ensure graph connectivity

    for i in range(n - 1):

        edges.append([
            locations[i],
            locations[i + 1],
            random.randint(1, 20)
        ])

    # Add additional random edges

    for _ in range(n * 2):

        u, v = random.sample(locations, 2)

        edges.append([
            u,
            v,
            random.randint(1, 20)
        ])

    return locations, edges


# Measure average execution time

def measure_time(function, repetitions=3):

    times = []

    for _ in range(repetitions):

        start = time.perf_counter()

        function()

        end = time.perf_counter()

        times.append(end - start)

    return sum(times) / len(times)


# Run benchmark

def run_benchmark():

    sizes = [10, 50, 100, 200]

    results = []

    print("\n========================================")
    print("       PERFORMANCE BENCHMARK")
    print("========================================")

    for n in sizes:

        print(f"\nTesting Dataset Size: {n}")

        parcels = generate_parcels(n)

        locations, edges = generate_graph(n)

        graph = build_graph(locations, edges)

        capacity = n * 5

        # 1. Merge Sort

        merge_time = measure_time(
            lambda: merge_sort(parcels)
        )

        # 2. Knapsack DP

        knapsack_time = measure_time(
            lambda: knapsack(parcels, capacity)
        )

        # 3. Dijkstra

        dijkstra_time = measure_time(
            lambda: dijkstra(graph, "W")
        )

        # 4. Prepare shortest distance matrix

        destinations = locations[1:]

        def prepare_matrix():

            matrix = {}

            for source in locations:

                dist, _ = dijkstra(graph, source)

                matrix[source] = dist

            return matrix

        distance_matrix = prepare_matrix()

        # 5. Nearest Neighbor TSP

        tsp_time = measure_time(
            lambda: nearest_neighbor_tsp(
                "W",
                destinations,
                distance_matrix
            )
        )

        # 6. Complete route planning time

        def complete_route():

            matrix = prepare_matrix()

            return nearest_neighbor_tsp(
                "W",
                destinations,
                matrix
            )

        route_time = measure_time(complete_route)

        results.append({
            "Dataset Size": n,
            "Merge Sort": merge_time,
            "Knapsack DP": knapsack_time,
            "Dijkstra": dijkstra_time,
            "TSP": tsp_time,
            "Complete Route Planning": route_time
        })

        print("Merge Sort:", round(merge_time, 6), "seconds")

        print("Knapsack DP:", round(knapsack_time, 6), "seconds")

        print("Dijkstra:", round(dijkstra_time, 6), "seconds")

        print("TSP:", round(tsp_time, 6), "seconds")

        print("Complete Route Planning:",
              round(route_time, 6), "seconds")

    # Save results

    os.makedirs("reports", exist_ok=True)

    with open(
        "reports/performance_results.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )

        writer.writeheader()

        writer.writerows(results)

    print("\n========================================")

    print("BENCHMARK COMPLETED SUCCESSFULLY")

    print("Results saved in reports/performance_results.csv")

    print("========================================")


if __name__ == "__main__":

    run_benchmark()