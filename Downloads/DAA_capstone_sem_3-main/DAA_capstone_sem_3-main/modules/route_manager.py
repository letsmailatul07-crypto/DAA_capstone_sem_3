import json
import time
from algorithms.tsp import nearest_neighbor_tsp

from algorithms.knapsack import knapsack

from modules.parcel_manager import load_parcels

from algorithms.dijkstra import (
    build_graph,
    dijkstra,
    reconstruct_path
)


def load_graph():

    with open("data/locations.json", "r") as file:

        data = json.load(file)

    graph = build_graph(
        data["locations"],
        data["edges"]
    )

    return graph


def display_graph():

    graph = load_graph()

    print("\n========== DELIVERY GRAPH ==========")

    for location, neighbors in graph.items():

        print(f"\n{location}:")

        for neighbor, distance in neighbors:

            print(
                f"  -> {neighbor} ({distance} km)"
            )


def find_shortest_path():

    graph = load_graph()

    print("\n========== DIJKSTRA SHORTEST PATH ==========")

    print("Available Locations:")

    print(", ".join(graph.keys()))

    source = input("\nEnter starting location: ").upper()

    destination = input("Enter destination: ").upper()

    if source not in graph or destination not in graph:

        print("Invalid location!")

        return

    start_time = time.perf_counter()

    dist, parent = dijkstra(graph, source)

    end_time = time.perf_counter()

    path = reconstruct_path(
        parent,
        source,
        destination
    )

    if not path:

        print("\nNo route exists between these locations.")

        return

    print("\n========== SHORTEST PATH RESULT ==========")

    print("Starting Location:", source)

    print("Destination:", destination)

    print("Shortest Path:", " -> ".join(path))

    print("Total Distance:", dist[destination], "km")

    print(
        "Execution Time:",
        round(end_time - start_time, 8),
        "seconds"
    )

def generate_delivery_route():

    graph = load_graph()

    parcels = load_parcels()

    capacity = 15

    # Step 1: Select parcels using Knapsack

    result = knapsack(parcels, capacity)

    selected_parcels = result["selected"]

    if not selected_parcels:

        print("No parcels selected!")

        return

    # Step 2: Get customer destinations

    destinations = list(dict.fromkeys(
        p["destination"] for p in selected_parcels
    ))

    start = "W"

    print("\n========== COURIER ROUTE OPTIMIZATION ==========")

    print("\nSelected Parcels:")

    for parcel in selected_parcels:

        print(
            parcel["id"],
            "->",
            parcel["destination"]
        )

    print("\nDestinations:", destinations)

    # Step 3: Calculate shortest distances using Dijkstra

    distance_matrix = {}

    path_matrix = {}

    start_time = time.perf_counter()

    required_locations = [start] + destinations

    for source in required_locations:

        dist, parent = dijkstra(graph, source)

        distance_matrix[source] = {}

        path_matrix[source] = {}

        for destination in required_locations:

            distance_matrix[source][destination] = dist[destination]

            path_matrix[source][destination] = reconstruct_path(
                parent,
                source,
                destination
            )

    # Step 4: Apply Nearest Neighbor TSP

    route, total_distance = nearest_neighbor_tsp(
        start,
        destinations,
        distance_matrix
    )

    end_time = time.perf_counter()

    # Step 5: Display route

    print("\n========== FINAL DELIVERY ROUTE ==========")

    print(" -> ".join(route))

    # Step 6: Display individual shortest paths

    print("\nDETAILED DELIVERY JOURNEY:")

    for i in range(len(route) - 1):

        u = route[i]

        v = route[i + 1]

        path = path_matrix[u][v]

        distance = distance_matrix[u][v]

        print(
            f"{u} -> {v}: "
            f"{' -> '.join(path)} "
            f"({distance} km)"
        )

    # Step 7: Display summary

    print("\n========== DELIVERY SUMMARY ==========")

    print("Total Parcels:", len(selected_parcels))

    print("Total Weight:", result["total_weight"], "kg")

    print("Total Parcel Value:", result["total_value"])

    print("Total Route Distance:", total_distance, "km")

    print(
        "Route Optimization Time:",
        round(end_time - start_time, 8),
        "seconds"
    )

    return route, total_distance