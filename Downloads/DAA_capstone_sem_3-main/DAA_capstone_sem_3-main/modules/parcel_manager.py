import json
import time
from algorithms.knapsack import knapsack

from algorithms.merge_sort import merge_sort


def load_parcels():

    with open("data/parcels.json", "r") as file:

        parcels = json.load(file)

    return parcels


def display_parcels(parcels):

    print("\n========== PARCEL LIST ==========")

    print("ID\tWeight\tValue\tPriority\tDeadline")

    for p in parcels:

        if p["priority"] == 3:
            priority = "High"

        elif p["priority"] == 2:
            priority = "Medium"

        else:
            priority = "Low"

        print(
            f'{p["id"]}\t'
            f'{p["weight"]}\t'
            f'{p["value"]}\t'
            f'{priority}\t\t'
            f'{p["deadline"]}'
        )


def sort_parcels():

    parcels = load_parcels()

    print("\nBefore Sorting:")

    display_parcels(parcels)

    start = time.perf_counter()

    sorted_parcels = merge_sort(parcels)

    end = time.perf_counter()

    print("\nAfter Sorting:")

    display_parcels(sorted_parcels)

    print("\nSorting Execution Time:",
          round(end - start, 8), "seconds")

    return sorted_parcels

def optimize_packages():

    parcels = load_parcels()

    capacity = 15

    print("\n========== KNAPSACK OPTIMIZATION ==========")

    print("Vehicle Capacity:", capacity, "kg")

    result = knapsack(parcels, capacity)

    # Display DP Table

    print("\nDP TABLE:")

    print("      ", end="")

    for w in range(capacity + 1):
        print(f"{w:4}", end="")

    print()

    for i, row in enumerate(result["dp_table"]):

        print(f"{i:4}  ", end="")

        for value in row:
            print(f"{value:4}", end="")

        print()

    # Selected parcels

    print("\nSELECTED PARCELS:")

    display_parcels(result["selected"])

    # Rejected parcels

    print("\nREJECTED PARCELS:")

    display_parcels(result["rejected"])

    print("\n========== PACKING SUMMARY ==========")

    print("Total Weight:",
          result["total_weight"], "kg")

    print("Total Value:",
          result["total_value"])

    print("Remaining Capacity:",
          result["remaining_capacity"], "kg")