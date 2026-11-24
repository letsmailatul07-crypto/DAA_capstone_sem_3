from modules.report_generator import generate_delivery_report

from modules.parcel_manager import sort_parcels, optimize_packages

from modules.route_manager import (
    display_graph,
    find_shortest_path,
    generate_delivery_route
)

from modules.report_generator import generate_delivery_report


def main():

    while True:

        print("\n==========================================")
        print("   INTELLIGENT COURIER OPTIMIZATION")
        print("==========================================")

        print("\n1. Sort Parcels")
        print("2. Optimize Package Selection")
        print("3. Display Delivery Graph")
        print("4. Find Shortest Path (Dijkstra)")
        print("5. Generate Optimized Delivery Route")
        print("6. Generate Delivery Report")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            sort_parcels()

        elif choice == "2":
            optimize_packages()

        elif choice == "3":
            display_graph()

        elif choice == "4":
            find_shortest_path()

        elif choice == "5":
            generate_delivery_route()

        elif choice == "6":
            generate_delivery_report()

        elif choice == "7":
            print("\nThank you for using Courier Optimization System!")
            break

        else:
            print("\nInvalid choice! Try again.")


if __name__ == "__main__":
    main()