def knapsack(parcels, capacity):

    n = len(parcels)

    # Create DP table
    dp = [[0 for _ in range(capacity + 1)]
          for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):

        weight = parcels[i - 1]["weight"]
        value = parcels[i - 1]["value"]

        for w in range(capacity + 1):

            if weight <= w:

                dp[i][w] = max(
                    value + dp[i - 1][w - weight],
                    dp[i - 1][w]
                )

            else:

                dp[i][w] = dp[i - 1][w]

    # Find selected parcels
    selected = []

    w = capacity

    for i in range(n, 0, -1):

        if dp[i][w] != dp[i - 1][w]:

            selected.append(parcels[i - 1])

            w -= parcels[i - 1]["weight"]

    selected.reverse()

    # Find rejected parcels
    selected_ids = {p["id"] for p in selected}

    rejected = [
        p for p in parcels
        if p["id"] not in selected_ids
    ]

    total_weight = sum(p["weight"] for p in selected)

    total_value = sum(p["value"] for p in selected)

    remaining_capacity = capacity - total_weight

    return {
        "selected": selected,
        "rejected": rejected,
        "total_weight": total_weight,
        "total_value": total_value,
        "remaining_capacity": remaining_capacity,
        "dp_table": dp
    }