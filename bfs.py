# HUFANA, MEZO, TAMPUGAO
# Task 3: Breadth-first search (BFS) in Python
# This program solves the 8-puzzle problem using Breadth-First Search (BFS).
# BFS explores states level by level to guarantee the shortest solution if one exists.

from collections import deque

class Node:
    def __init__(self, state, parent=None):
        
        # Node represents a puzzle state and keeps track of its parent to reconstruct the path once the goal is found.
        
        self.state = state
        self.parent = parent

    def path(self):
        
        # Reconstruct the path from the root node to this node.
        
        node, path_list = self, []
        while node:
            path_list.append(node)
            node = node.parent
        return path_list[::-1]  # reverse so root -> goal,  Returns the path as a list of nodes (from start to goal).


def print_board(state):
    
    # print a board state in a 3x3 format.
    
    for row in state:
        print(" ".join(str(tile) for tile in row))
    print()


def find_empty(state):
    
    # Find the (row, col) position of the blank (represented by 0).
    
    for row_index in range(3):
        for col_index in range(3):
            if state[row_index][col_index] == 0:
                return row_index, col_index
    return None


def get_neighbors(state):

    # Generate all valid neighbor states by moving the blank tile.

    empty_row, empty_col = find_empty(state)
    neighbors = []

    # Possible moves: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for row_offset, col_offset in directions:
        new_row, new_col = empty_row + row_offset, empty_col + col_offset

        # Ensure new position is inside the 3x3 board
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = [list(row) for row in state]  # deep copy
            # Swap blank with the tile in the new position
            new_state[empty_row][empty_col], new_state[new_row][new_col] = (
                new_state[new_row][new_col],
                new_state[empty_row][empty_col],
            )
            neighbors.append(new_state)

    return neighbors # Returns a list of neighboring states.


def serialize(state):
    
    # Convert a 2D board state into a string for hashing/comparison.
    # Example: [[1,2,3],[4,5,6],[7,8,0]] -> "123456780"
    
    return "".join(str(tile) for row in state for tile in row)


def is_solvable(state):
    
    # Check if the puzzle is solvable using the inversion count method.
    # If the number of inversions is even -> solvable.
    
    flat_list = [num for row in state for num in row if num != 0]
    inversions = 0
    for i in range(len(flat_list)):
        for j in range(i + 1, len(flat_list)):
            if flat_list[i] > flat_list[j]:
                inversions += 1
    return inversions % 2 == 0


def bfs(initial_state, goal_state, state_space):
    
    # Perform Breadth-First Search (BFS) from the initial state to the goal state.
    # Tracks visited states and state transitions in state_space.
    
    root = Node(initial_state)
    if root.state == goal_state:
        print("GOAL FOUND at Level 0")
        return root, 0

    frontier = deque([root])  # queue for BFS
    explored = set()          # visited states
    level = 0                 # BFS depth level

    while frontier:
        level_size = len(frontier)
        print(f"\n--- BFS Level {level} ---")

        for _ in range(level_size):
            node = frontier.popleft()
            explored.add(serialize(node.state))

            print_board(node.state)  # Display current node’s board

            # Generate neighbors and record transitions
            neighbors = get_neighbors(node.state)
            state_space[serialize(node.state)] = [serialize(neighbor) for neighbor in neighbors]

            for neighbor in neighbors:
                if serialize(neighbor) in explored:
                    continue
                child = Node(neighbor, node)

                # Goal check
                if neighbor == goal_state:
                    print("\nGOAL FOUND at Level", level + 1)
                    return child, level + 1

                frontier.append(child)

        level += 1

    return None, None # Returns the goal node and BFS level if found, else (None, None).


def read_input_file(filename):
    
    # Read initial and goal states from a text file.
    # File format: 6 lines -> first 3 lines = initial state, next 3 lines = goal state.
    # Blank tile should be represented by 0 or space.
    
    with open(filename, "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    if len(lines) != 6:
        raise ValueError("File must contain exactly 6 lines (3 for initial, 3 for goal)")

    def parse_board(board_lines):
        return [[int(tile) if tile != " " else 0 for tile in line.split(",")] for line in board_lines]

    initial_state = parse_board(lines[:3])
    goal_state = parse_board(lines[3:])
    return initial_state, goal_state


def main():
    """
    Main function to run the BFS 8-puzzle solver.
    Reads input, validates solvability, runs BFS, and prints solution path.
    """
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
    except Exception as error:
        print("Error reading file:", error)
        return

    print("Initial State:")
    print_board(initial_state)
    print("Goal State:")
    print_board(goal_state)

    if not is_solvable(initial_state):
        print("This puzzle is unsolvable.")
        return

    state_space = {}  # Dictionary to hold state transitions

    print("\nRunning BFS...\n")
    solution_node, goal_level = bfs(initial_state, goal_state, state_space)

    if not solution_node:
        print("No solution found.")
        return

    # Print the solution path
    path = solution_node.path()
    print("\n✅ Solution Path:\n")
    for step_index, node in enumerate(path):
        print(f"Step {step_index}:")
        print_board(node.state)

    print(f"Total moves = {len(path) - 1}")
    print(f"Goal reached at BFS Level {goal_level}")


if __name__ == "__main__":
    main()
