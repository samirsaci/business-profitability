"""
Business Profitability Optimization

This script uses linear programming to maximize bakery profits
by determining optimal production quantities for each product.
"""

import pandas as pd
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, value


def create_bakery_model():
    """Create and solve the bakery profit maximization model."""
    # Product data
    products = {
        "Croissant": {"profit": 0.90, "baker": 5, "oven": 5, "assistant": 0, "display": 1},
        "Chocolate Bread": {"profit": 1.00, "baker": 6, "oven": 7, "assistant": 0, "display": 1},
        "Cake Slice": {"profit": 6.00, "baker": 30, "oven": 30, "assistant": 0, "display": 2},
        "Fancy Cake": {"profit": 15.00, "baker": 60, "oven": 60, "assistant": 0, "display": 6},
        "Bread": {"profit": 1.50, "baker": 5, "oven": 12, "assistant": 0, "display": 1},
        "Sandwich": {"profit": 4.40, "baker": 2, "oven": 0, "assistant": 10, "display": 1},
    }

    # Resources available (in minutes)
    resources = {
        "baker": 4 * 6 * 60,  # 4 bakers, 6 hours each
        "oven": 2 * 24 * 60,  # 2 ovens, 24 hours each
        "assistant": 4 * 60,  # 1 assistant, 4 hours
        "display": 100,  # 100 display slots
    }

    # Initialize model
    model = LpProblem("Bakery_Profit_Maximization", LpMaximize)

    # Decision variables: quantity of each product to produce
    x = LpVariable.dicts(
        "quantity", products.keys(), lowBound=0, cat="Integer"
    )

    # Objective: maximize total profit
    model += lpSum([products[p]["profit"] * x[p] for p in products])

    # Constraints: resource limitations
    model += (
        lpSum([products[p]["baker"] * x[p] for p in products]) <= resources["baker"],
        "Baker_Time",
    )
    model += (
        lpSum([products[p]["oven"] * x[p] for p in products]) <= resources["oven"],
        "Oven_Time",
    )
    model += (
        lpSum([products[p]["assistant"] * x[p] for p in products])
        <= resources["assistant"],
        "Assistant_Time",
    )
    model += (
        lpSum([products[p]["display"] * x[p] for p in products])
        <= resources["display"],
        "Display_Space",
    )

    # Solve
    model.solve()

    return model, x, products, resources


def display_results(model, x, products, resources):
    """Display optimization results."""
    print("=" * 60)
    print("BAKERY PROFIT OPTIMIZATION RESULTS")
    print("=" * 60)
    print(f"\nStatus: {LpStatus[model.status]}")
    print(f"Maximum Daily Profit: €{value(model.objective):.2f}")

    print("\n" + "-" * 60)
    print("OPTIMAL PRODUCTION QUANTITIES")
    print("-" * 60)

    total_items = 0
    for product in products:
        qty = int(x[product].varValue) if x[product].varValue else 0
        profit = qty * products[product]["profit"]
        if qty > 0:
            print(f"  {product}: {qty} units (€{profit:.2f})")
            total_items += qty

    print(f"\nTotal items to produce: {total_items}")

    print("\n" + "-" * 60)
    print("RESOURCE UTILIZATION")
    print("-" * 60)

    for resource in resources:
        used = sum(
            products[p][resource] * (x[p].varValue or 0) for p in products
        )
        available = resources[resource]
        utilization = (used / available) * 100
        print(f"  {resource.capitalize()}: {used:.0f}/{available} min ({utilization:.1f}%)")


def main():
    """Main function to run the optimization."""
    model, x, products, resources = create_bakery_model()
    display_results(model, x, products, resources)


if __name__ == "__main__":
    main()
