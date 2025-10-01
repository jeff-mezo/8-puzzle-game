# HUFANA, MEZO, TAMPUGAO
# Task 3: Breadth-first search (BFS) in Python

from collections import deque

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

    def path(self):
        # Reconstruct path from root to this node
        node, path_list = self, []
        while node:
            path_list.append(node)
            node = node.parent
        return path_list[::-1]  # reverse order


def print_board(state):
    # Print a board state
    for row in state:
        print(" ".join(str(x) for x in row))
    print()


def find_empty(state):
    # Find position of blank (0)
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c
    return None


def get_neighbors(state):
    # Generate all valid neighbor states
    r, c = find_empty(state)
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_state = [list(row) for row in state]
            new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
            moves.append(new_state)
    return moves


def serialize(state):
    # Convert board to string for hashing
    return "".join(str(x) for row in state for x in row)


def is_solvable(state):
    # Check solvability using inversion count
    flat = [num for row in state for num in row if num != 0]
    inversions = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inversions += 1
    return inversions % 2 == 0


def bfs(initial_state, goal_state, state_space):
    # Breadth-First Search
    root = Node(initial_state)
    if root.state == goal_state:
        print("GOAL FOUND at Level 0")
        return root, 0

    frontier = deque([root])
    explored = set()
    level = 0

    while frontier:
        level_size = len(frontier)
        print(f"\n--- BFS Level {level} ---")

        for _ in range(level_size):
            node = frontier.popleft()
            explored.add(serialize(node.state))

            print_board(node.state)  # show node

            # Record state transitions
            neighbors = get_neighbors(node.state)
            state_space[serialize(node.state)] = [serialize(n) for n in neighbors]

            for neighbor in neighbors:
                if serialize(neighbor) in explored:
                    continue
                child = Node(neighbor, node)
                if neighbor == goal_state:
                    print("\nGOAL FOUND at Level", level + 1)
                    return child, level + 1
                frontier.append(child)

        level += 1

    return None, None


def read_input_file(filename):
    # Read initial and goal states from file
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    if len(lines) != 6:
        raise ValueError("File must contain exactly 6 lines (3 for initial, 3 for goal)")

    def parse_board(lines):
        return [[int(x) if x != " " else 0 for x in line.split(",")] for line in lines]

    initial = parse_board(lines[:3])
    goal = parse_board(lines[3:])
    return initial, goal


def main():
    print("Breadth-First Search (BFS) for 8-Puzzle")
    print("--------------------------------------")
    print("BFS explores states level by level, ensuring shortest solution.")
    print("To start, type a file that has exactly 6 lines (3 for initial, 3 for goal)\n")
    print("Example input file (input.txt):")
    print("  1,2,3 --> Initial state")
    print("  4,0,6")
    print("  7,5,8\n")
    print("  1,2,3 --> Goal state")
    print("  4,5,6")
    print("  7,8,0\n")
    filename = input("Enter input filename. e.g. (C:\\Users\\input.txt): ").strip()
    try:
        initial_state, goal_state = read_input_file(filename)
    except Exception as e:
        print("Error reading file:", e)
        return

    print("Initial State:")
    print_board(initial_state)
    print("Goal State:")
    print_board(goal_state)

    if not is_solvable(initial_state):
        print("This puzzle is unsolvable.")
        return

    state_space = {}  # holds state transitions

    print("\nRunning BFS...\n")
    solution, goal_level = bfs(initial_state, goal_state, state_space)

    if not solution:
        print("No solution found.")
        return

    # Print solution path
    path = solution.path()
    print("\nSolution Path:\n")
    for i, node in enumerate(path):
        print(f"Step {i}:")
        print_board(node.state)

    print(f"Total moves = {len(path) - 1}")
    print(f"Goal reached at BFS Level {goal_level}")


if __name__ == "__main__":
    main()
