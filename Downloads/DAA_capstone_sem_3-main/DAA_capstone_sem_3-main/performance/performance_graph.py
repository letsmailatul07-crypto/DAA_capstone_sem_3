import csv
import os
import matplotlib.pyplot as plt


def generate_graph():

    sizes = []

    algorithms = {
        "Merge Sort": [],
        "Knapsack DP": [],
        "Dijkstra": [],
        "TSP": [],
        "Complete Route Planning": []
    }

    with open(
        "reports/performance_results.csv",
        "r"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            sizes.append(int(row["Dataset Size"]))

            for algorithm in algorithms:

                algorithms[algorithm].append(
                    float(row[algorithm])
                )

    os.makedirs("reports", exist_ok=True)

    # Individual graphs

    for algorithm, times in algorithms.items():

        plt.figure(figsize=(9, 5))

        plt.plot(
            sizes,
            times,
            marker="o",
            label=algorithm
        )

        plt.xlabel("Dataset Size")

        plt.ylabel("Execution Time (seconds)")

        plt.title(algorithm + " Performance Analysis")

        plt.legend()

        plt.grid(True)

        filename = algorithm.lower().replace(" ", "_")

        plt.savefig(
            f"reports/{filename}_performance.png"
        )

        plt.close()

    # Combined comparison graph

    plt.figure(figsize=(10, 6))

    for algorithm, times in algorithms.items():

        plt.plot(
            sizes,
            times,
            marker="o",
            label=algorithm
        )

    plt.xlabel("Dataset Size")

    plt.ylabel("Execution Time (seconds)")

    plt.title("Algorithm Performance Comparison")

    plt.yscale("log")

    plt.legend()

    plt.grid(True)

    plt.savefig(
        "reports/algorithm_comparison.png"
    )

    plt.close()

    print("\nPerformance graphs generated successfully!")

    print("Check the reports folder.")


if __name__ == "__main__":

    generate_graph()