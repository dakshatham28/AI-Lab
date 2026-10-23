
# Name: DAKSHATHA M
# USN: 1WA24CS102
# Experiment: Week-5 - Simulated Annealing for 8-Queens

import random
import math


def get_cost(state):
    """Count pairs of queens attacking diagonally."""
    cost = 0
    n = len(state)

    for i in range(n):
        for j in range(i + 1, n):
            if abs(i - j) == abs(state[i] - state[j]):
                cost += 1

    return cost


def simulated_annealing():
    print("Name: DAKSHATHA M")
    print("USN: 1WA24CS102")
    print("Simulated Annealing - 8 Queens")
    print("-" * 40)

    user_input = input(
        "Enter 8 queen positions (0-7), separated by spaces: "
    ).strip()

    if not user_input:
        current = [random.randint(0, 7) for _ in range(8)]
        print("Random initial state:", current)
    else:
        try:
            current = [int(x) for x in user_input.split()]
        except ValueError:
            print("Invalid input! Enter integer values.")
            return

        if len(current) != 8 or any(x < 0 or x > 7 for x in current):
            print("Invalid input! Enter exactly 8 values from 0 to 7.")
            return

    current_cost = get_cost(current)
    temperature = 100.0
    cooling_rate = 0.995
    max_iterations = 100000

    print("Initial state:", current)
    print("Initial cost:", current_cost)

    for step in range(max_iterations):
        if current_cost == 0:
            print("\nSolution found!")
            print("Final state:", current)
            print("Final cost:", current_cost)
            print("Iterations:", step)
            return

        # Generate a neighbor by moving one queen
        neighbor = current.copy()
        col = random.randint(0, 7)

        new_row = random.randint(0, 7)
        while new_row == neighbor[col]:
            new_row = random.randint(0, 7)

        neighbor[col] = new_row
        neighbor_cost = get_cost(neighbor)

        delta = neighbor_cost - current_cost

        # Accept better states or probabilistically accept worse states
        if delta < 0:
            current = neighbor
            current_cost = neighbor_cost
        elif random.random() < math.exp(-delta / temperature):
            current = neighbor
            current_cost = neighbor_cost

        # Reduce temperature
        temperature *= cooling_rate

        if temperature < 0.000001:
            temperature = 0.000001

    print("\nIteration limit reached.")
    print("Final state:", current)
    print("Final cost:", current_cost)

    if current_cost == 0:
        print("Solution found!")
    else:
        print("Solution not found. Try running again.")


if __name__ == "__main__":
    simulated_annealing()

