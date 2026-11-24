import json
import os
from datetime import datetime

from algorithms.knapsack import knapsack
from algorithms.dijkstra import (
    build_graph,
    dijkstra,
    reconstruct_path
)
from algorithms.tsp import nearest_neighbor_tsp


def generate_delivery_report():

    # Load parcel data
    with open("data/parcels.json", "r") as file:
        parcels = json.load(file)

    # Load location data
    with open("data/locations.json", "r") as file:
        location_data = json.load(file)

    locations = location_data["locations"]
    edges = location_data["edges"]

    # Vehicle capacity
    capacity = 15

    # Step 1: Select parcels using Knapsack
    packing = knapsack(parcels, capacity)

    selected = packing["selected"]
    rejected = packing["rejected"]

    # Step 2: Build delivery graph
    graph = build_graph(locations, edges)

    # Step 3: Get unique delivery destinations
    destinations = list(dict.fromkeys(
        parcel["destination"] for parcel in selected
    ))

    points = ["W"] + destinations

    # Step 4: Calculate shortest distances
    distance_matrix = {}
    path_matrix = {}

    for source in points:

        dist, parent = dijkstra(graph, source)

        distance_matrix[source] = {}
        path_matrix[source] = {}

        for destination in points:

            distance_matrix[source][destination] = dist[destination]

            path_matrix[source][destination] = (
                reconstruct_path(parent, source, destination)
            )

    # Step 5: Generate delivery route
    route, total_distance = nearest_neighbor_tsp(
        "W",
        points,
        distance_matrix
    )

    # Step 6: Create report
    report = []

    report.append("=" * 55)
    report.append("       INTELLIGENT COURIER OPTIMIZATION SYSTEM")
    report.append("                 DELIVERY REPORT")
    report.append("=" * 55)

    report.append(
        "\nGenerated On: " + datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    )

    report.append("\n1. VEHICLE INFORMATION")
    report.append("-" * 40)
    report.append(f"Vehicle Capacity: {capacity} kg")
    report.append(f"Total Loaded Weight: {packing['total_weight']} kg")
    report.append(f"Remaining Capacity: {packing['remaining_capacity']} kg")

    report.append("\n2. SELECTED PARCELS")
    report.append("-" * 40)

    for parcel in selected:
        report.append(
            f"{parcel['id']} | Weight: {parcel['weight']} kg | "
            f"Value: {parcel['value']} | "
            f"Destination: {parcel['destination']}"
        )

    report.append(f"\nTotal Selected Parcels: {len(selected)}")
    report.append(f"Total Parcel Value: {packing['total_value']}")

    report.append("\n3. REJECTED PARCELS")
    report.append("-" * 40)

    for parcel in rejected:
        report.append(
            f"{parcel['id']} | Weight: {parcel['weight']} kg | "
            f"Value: {parcel['value']}"
        )

    report.append(f"\nTotal Rejected Parcels: {len(rejected)}")

    report.append("\n4. OPTIMIZED DELIVERY ROUTE")
    report.append("-" * 40)
    report.append(" -> ".join(route))

    report.append(f"\nTotal Delivery Distance: {total_distance} km")

    report.append("\n5. SHORTEST PATH DETAILS")
    report.append("-" * 40)

    for i in range(len(route) - 1):

        source = route[i]
        destination = route[i + 1]

        path = path_matrix[source][destination]
        distance = distance_matrix[source][destination]

        report.append(
            f"{source} -> {destination}: "
            f"{' -> '.join(path)} ({distance} km)"
        )

    report.append("\n" + "=" * 55)
    report.append("             END OF DELIVERY REPORT")
    report.append("=" * 55)

    # Step 7: Save report
    os.makedirs("reports", exist_ok=True)

    report_path = "reports/delivery_report.txt"

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("\n".join(report))

    print("\nDelivery report generated successfully!")
    print("Saved at:", report_path)

    print("\n========== DELIVERY REPORT ==========")

    for line in report:
        print(line)