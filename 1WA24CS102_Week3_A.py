print("Name: DAKSHATHA M")
print("USN: 1WA24CS102")
print()

import heapq
import sys
sys.setrecursionlimit(20000)

def parse_input_state(prompt_text):
    print(prompt_text)
    print("Enter 9 numbers (0-8) separated by spaces (0 represents the blank space):")
    while True:
        try:
            user_input = input(">> ").strip().split()
            if len(user_input) != 9:
                print("Error: Please enter exactly 9 numbers.")
                continue
            numbers = [int(x) for x in user_input]
            if sorted(numbers) != list(range(9)):
                print("Error: Input must contain numbers from 0 to 8 exactly once.")
                continue

            return (
                tuple(numbers[0:3]),
                tuple(numbers[3:6]),
                tuple(numbers[6:9])
            )
        except ValueError:
            print("Error: Invalid characters. Please enter numbers only.")
def get_neighbors(board):
    neighbors = []
    br, bc = next(
        (r, c)
        for r in range(3)
        for c in range(3)
        if board[r][c] == 0
    )
    moves = [
        (-1, 0, "Up"),
        (1, 0, "Down"),
        (0, -1, "Left"),
        (0, 1, "Right")
    ]
    for dr, dc, move_name in moves:
        nr, nc = br + dr, bc + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_board = [list(row) for row in board]
            new_board[br][bc], new_board[nr][nc] = \
                new_board[nr][nc], new_board[br][bc]
            new_board_tuple = tuple(
                tuple(row) for row in new_board
            )
            neighbors.append(
                (new_board_tuple, move_name)
            )
    return neighbors
def print_board(board):
    for row in board:
        print(
            "   " +
            " ".join(
                str(x) if x != 0 else "_"
                for x in row
            )
        )
    print()
def is_solvable(start, goal):
    def count_inversions(board):
        flat_list = [
            num
            for row in board
            for num in row
            if num != 0
        ]
        inversions = 0
        for i in range(len(flat_list)):
            for j in range(i + 1, len(flat_list)):
                if flat_list[i] > flat_list[j]:
                    inversions += 1
        return inversions
    return (
        count_inversions(start) % 2
        ==
        count_inversions(goal) % 2
    )
def manhattan_distance(board, goal):
    """Calculate h(n) using Manhattan Distance."""
    goal_positions = {}
    for r in range(3):
        for c in range(3):
            goal_positions[goal[r][c]] = (r, c)
    distance = 0
    for r in range(3):
        for c in range(3):
            value = board[r][c]
            if value != 0:
                gr, gc = goal_positions[value]
                distance += abs(r - gr) + abs(c - gc)
    return distance
def a_star_search(initial_state, goal_state):
    """Solves the 8-puzzle using A* Search."""
    counter = 0
    initial_h = manhattan_distance(
        initial_state,
        goal_state
    )
    # (f, counter, g, board, path)
    priority_queue = [
        (
            initial_h,
            counter,
            0,
            initial_state,
            [(initial_state, "Start")]
        )
    ]
    best_cost = {
        initial_state: 0
    }
    while priority_queue:
        f, _, g, current_board, current_path = \
            heapq.heappop(priority_queue)
        if current_board == goal_state:
            return current_path
        if g > best_cost.get(current_board, float("inf")):
            continue
        for neighbor_board, move_name in get_neighbors(
                current_board):
            new_g = g + 1
            if new_g < best_cost.get(
                    neighbor_board,
                    float("inf")):
                best_cost[neighbor_board] = new_g
                h = manhattan_distance(
                    neighbor_board,
                    goal_state
                )
                new_f = new_g + h
                counter += 1
                new_path = current_path + [
                    (neighbor_board, move_name)
                ]
                heapq.heappush(
                    priority_queue,
                    (
                        new_f,
                        counter,
                        new_g,
                        neighbor_board,
                        new_path
                    )
                )
    return None
if __name__ == "__main__":
    print("8-Puzzle A* Search Solver\n")
    initial_state = parse_input_state(
        "Define Initial State"
    )
    goal_state = parse_input_state(
        "\nDefine Goal State"
    )
    if not is_solvable(initial_state, goal_state):
        print(
            "\n[!] Calculation Stopped: "
            "The initial state cannot mathematically reach "
            "that goal state."
        )
    else:
        solution = a_star_search(
            initial_state,
            goal_state
        )
        if solution:
            path_cost = len(solution) - 1
            print(

            )
            for step_idx, (board, move) in enumerate(solution):
                # g(n)
                g = step_idx
                # h(n)
                h = manhattan_distance(
                    board,
                    goal_state
                )
                # f(n) = g(n) + h(n)
                f = g + h
                if step_idx == 0:
                    print("Initial Setup:")
                else:
                    print(
                        f"Step {step_idx}: "
                        f"Move Empty Spot '{move}'"
                    )
                print(
                    f"g(n) = {g}, "
                    f"h(n) = {h}, "
                    f"f(n) = {f}"
                )
                print_board(board)
            print("-" * 40)
        else:
            print(
                "\nNo solution was found."
            )
