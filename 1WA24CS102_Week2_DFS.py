print("Name: DAKSHATHA M")
print("USN: 1WA24CS102")
print()

import sys
sys.setrecursionlimit(20000)
def parse_input_state(prompt_text):
    """Parses user input into a 3x3 tuple format."""
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
    """Generates all valid adjacent board configurations."""
    neighbors = []
    br, bc = next((r, c) for r in range(3) for c in range(3) if board[r][c] == 0)
    moves = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]
    for dr, dc, move_name in moves:
        nr, nc = br + dr, bc + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_board = [list(row) for row in board]
            new_board[br][bc], new_board[nr][nc] = new_board[nr][nc], new_board[br][bc]
            new_board_tuple = tuple(tuple(row) for row in new_board)
            neighbors.append((new_board_tuple, move_name))
    return neighbors
def print_board(board):
    """Formats the grid for presentation."""
    for row in board:
        print("   " + " ".join(str(x) if x != 0 else "_" for x in row))
    print()
def is_solvable(start, goal):
    """Checks if inversion parity matches between start and goal states."""
    def count_inversions(board):
        flat_list = [num for row in board for num in row if num != 0]
        inversions = 0
        for i in range(len(flat_list)):
            for j in range(i + 1, len(flat_list)):
                if flat_list[i] > flat_list[j]:
                    inversions += 1
        return inversions
    return (count_inversions(start) % 2) == (count_inversions(goal) % 2)
def dfs_find_all_paths(current_board, goal_board, visited, current_path, all_paths, max_depth):
    """Recursive DFS function to find all unique valid paths within a depth threshold."""
    if current_board == goal_board:
        all_paths.append(list(current_path))
        return
    if len(current_path) - 1 >= max_depth:
        return
    for neighbor_board, move_name in get_neighbors(current_board):
        if neighbor_board not in visited:
            visited.add(neighbor_board)
            current_path.append((neighbor_board, move_name))
            dfs_find_all_paths(neighbor_board, goal_board, visited, current_path, all_paths, max_depth)
            current_path.pop()
            visited.remove(neighbor_board)
if __name__ == "__main__":
    print("=== 8-Puzzle DFS Multi-Path Solver ===\n")
    initial_state = parse_input_state("--- Define Initial State ---")
    goal_state = parse_input_state("\n--- Define Goal State ---")
    print("\nValidating board match capability...")
    if not is_solvable(initial_state, goal_state):
        print("\n[!] Calculation Stopped: The initial state cannot mathematically reach that goal state.")
    else:
        MAX_DEPTH_LIMIT = 12
        print(f"Executing Depth-First Search (Depth limit restricted to {MAX_DEPTH_LIMIT} steps)...")
        discovered_paths = []
        tracking_visited = {initial_state}
        initial_history = [(initial_state, "Start")]
        dfs_find_all_paths(
            initial_state,
            goal_state,
            tracking_visited,
            initial_history,
            discovered_paths,
            MAX_DEPTH_LIMIT
        )
        if discovered_paths:
            print(f"\n[Success] DFS found {len(discovered_paths)} unique paths within depth limit!")
            discovered_paths.sort(key=len)
            for path_index, path in enumerate(discovered_paths, 1):
                path_cost = len(path) - 1
                print(f"\n=== DFS PATH WAY #{path_index} (Total Path Cost: {path_cost} steps) ===")
                for step_idx, (board, move) in enumerate(path):
                    if step_idx == 0:
                        print("Initial Setup:")
                    else:
                        print(f"Step {step_idx}: Move Empty Spot '{move}'")
                    print_board(board)
                print("-" * 40)
        else:
            print(f"\nNo paths discovered using DFS within a limit of {MAX_DEPTH_LIMIT} steps.")
            print("Try testing states that are fewer moves apart or increase the MAX_DEPTH_LIMIT threshold.")
