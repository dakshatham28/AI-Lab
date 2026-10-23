
# Name: DAKSHATHA M
# USN: 1WA24CS102
# Experiment: Week-4 Hill Climbing for 4-Queens

def get_cost(state):
    """Calculates the total number of diagonal conflict pairs."""
    cost = 0
    n = len(state)

    for i in range(n):
        for j in range(i + 1, n):
            if abs(i - j) == abs(state[i] - state[j]):
                cost += 1

    return cost


def format_state_string(state):
    """Formats a state array into x_0=val, x_1=val..."""
    return ", ".join(
        [f"x_{idx} = {val}" for idx, val in enumerate(state)]
    )


def run_hill_climbing_4_queens():
    print("Name: DAKSHATHA M")
    print("USN: 1WA24CS102")
    print("Experiment: Week-4 Hill Climbing - 4 Queens")
    print("-" * 50)

    print("Enter initial queen positions for rows 0, 1, 2, 3.")
    print("Example: 3 1 2 0")
    user_input = input("Initial positions: ").strip()

    # Default initial configuration
    if not user_input:
        state = [3, 1, 2, 0]
    else:
        state = [int(x) for x in user_input.split()]

    if len(state) != 4 or any(x not in range(4) for x in state):
        print("Invalid input! Enter exactly 4 values from 0 to 3.")
        return

    current_cost = get_cost(state)
    n = len(state)

    print(
        f"\nSolution: Neighbours of "
        f"{format_state_string(state)} "
        f"(cost is {current_cost}.)\n"
    )

    while current_cost > 0:
        neighbors_list = []

        # Generate all pairs of swaps in lexicographical order
        for i in range(n):
            for j in range(i + 1, n):
                neighbor_state = list(state)

                neighbor_state[i], neighbor_state[j] = (
                    neighbor_state[j], neighbor_state[i]
                )

                cost = get_cost(neighbor_state)

                neighbors_list.append({
                    'pair': (i, j),
                    'state': neighbor_state,
                    'cost': cost,
                    'text': format_state_string(neighbor_state)
                })

        # Find the minimum cost among neighbors
        min_cost = min(item['cost'] for item in neighbors_list)

        # Select the first neighbor with minimum cost
        chosen_neighbor = None

        for item in neighbors_list:
            if item['cost'] == min_cost:
                chosen_neighbor = item
                break

        # Display all neighbors and their costs
        for item in neighbors_list:
            action_text = ""

            if (item == chosen_neighbor
                    and min_cost < current_cost):
                action_text = " Choose this neighbour."

            print(
                f"  • {item['text']} "
                f"cost is {item['cost']}.{action_text}"
            )

        # Move only if cost improves
        if min_cost < current_cost:
            state = chosen_neighbor['state']
            current_cost = chosen_neighbor['cost']

            if current_cost > 0:
                print(
                    f"\nNeighbours of {format_state_string(state)} "
                    f"(cost is {current_cost}.)\n"
                )
        else:
            print("\nLocal optimum reached. No better neighbor found.")
            break

    print("\n" + "-" * 50)
    print("Name: DAKSHATHA M")
    print("USN: 1WA24CS102")
    print("Final state:", state)
    print("Final cost:", current_cost)

    if current_cost == 0:
        print("Goal configuration reached!")
    else:
        print("Goal configuration not reached.")


if __name__ == "__main__":
    run_hill_climbing_4_queens()
