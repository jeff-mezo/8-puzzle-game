import heapq # For implementing priority queue without manual sorting

# initial_state = []
# goal_state = []
# state_space = {}

class Node:
    def __init__(self, state, parent=None, g_cost=0, h_cost=0):
        self.state = state
        self.parent = parent
        self.g_cost = g_cost  # Cost from start to current node
        self.h_cost = h_cost  # Heuristic cost from current node to goal
        self.f_cost = g_cost + h_cost  # Total cost

    def __lt__(self, other):
        return self.f_cost < other.f_cost

def a_star_search(initial_state, goal_state, get_neighbors_func, heuristic_func):
    """
    Performs the A* search to find the shortest path from an initial state
    to a goal state.
    """
    open_list = [] # priority queue for nodes to explore
    closed_list = set() # explored nodes

    initial_h_cost = heuristic_func(initial_state, goal_state)
    start_node = Node(state=initial_state, g_cost=0, h_cost=initial_h_cost) # starting node
    heapq.heappush(open_list, start_node) # add start node to open list

    while open_list:
        current_node = heapq.heappop(open_list) # get node with lowest f_cost

        # If the node has already been explored, skip it
        if current_node.state in closed_list:
            continue
        
        closed_list.add(current_node.state)

        # Check if we reached the goal
        if current_node.state == goal_state:
            path = []
            temp = current_node
            while temp:
                path.append(temp.state)
                temp = temp.parent
            return path[::-1]

        # Explore neighbors
        for neighbor_state, move_cost in get_neighbors_func(current_node.state):
            if neighbor_state in closed_list:
                continue

            g_cost = current_node.g_cost + move_cost # cost from start to neighbor
            h_cost = heuristic_func(neighbor_state, goal_state) # heuristic cost from neighbor to goal
            
            neighbor_node = Node(state=neighbor_state, parent=current_node, g_cost=g_cost, h_cost=h_cost) # create neighbor node  
            heapq.heappush(open_list, neighbor_node) # add neighbor to open list

    return None # return None if no path is found


# --------------------------------------------------------------------------
# Helper functions for the 8-Puzzle Game
# --------------------------------------------------------------------------

def parse_puzzle_file(filename):
    """Reads the puzzle.txt file and returns the initial and goal states."""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    
    initial_idx = lines.index('initial:') + 1
    goal_idx = lines.index('goal:') + 1

    initial_state = tuple(tuple(map(int, row.split(','))) for row in lines[initial_idx:initial_idx+3])
    goal_state = tuple(tuple(map(int, row.split(','))) for row in lines[goal_idx:goal_idx+3])
    
    return initial_state, goal_state

def calculate_manhattan_distance(state, goal_state):
    """Heuristic function: Calculates the Manhattan distance for the 8-puzzle."""
    h_cost = 0
    goal_positions = {tile: (r, c) for r, row in enumerate(goal_state) for c, tile in enumerate(row)}

    for r in range(3):
        for c in range(3):
            tile = state[r][c]
            if tile != 0:
                goal_r, goal_c = goal_positions[tile]
                h_cost += abs(r - goal_r) + abs(c - goal_c)
    return h_cost

def get_neighbors(state):
    """Generates all valid neighbor states by moving the blank tile (0)."""
    neighbors = []
    
    # Find the position of the blank tile (0)
    blank_pos = None
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                blank_pos = (r, c)
                break
        if blank_pos:
            break
            
    r, c = blank_pos
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        
        if 0 <= nr < 3 and 0 <= nc < 3:
            # Create a mutable copy (list of lists)
            new_state_list = [list(row) for row in state]
            # Swap the tiles
            new_state_list[r][c], new_state_list[nr][nc] = new_state_list[nr][nc], new_state_list[r][c]
            # Convert back to immutable tuple of tuples to be hashable
            new_state_tuple = tuple(tuple(row) for row in new_state_list)
            # Each move has a cost of 1
            neighbors.append((new_state_tuple, 1))
            
    return neighbors

def print_board(state, step):
    """Prints the 3x3 board state beautifully."""
    print(f"--- Step {step} ---")
    for row in state:
        print(" ".join(map(str, row)))
    print()

# --------------------------------------------------------------------------
# Task 3 - A* Algorithm for 8-Puzzle Game
# --------------------------------------------------------------------------
if __name__ == "__main__":
    
    print("--- A* Algorithm for 8-Puzzle Game ---")
    
    # 1. Get initial and goal states from the file
    try:
        initial_state, goal_state = parse_puzzle_file('puzzle.txt')
    except FileNotFoundError:
        print("Error: puzzle.txt not found. Please create the file as specified.")
        exit()
        
    print("Initial State:")
    print_board(initial_state, 0)
    
    print("Goal State:")
    for row in goal_state:
        print(" ".join(map(str, row)))
    print("\nSolving...\n")
    
    # 2. Run the A* algorithm
    final_path = a_star_search(
        initial_state, 
        goal_state, 
        get_neighbors, 
        calculate_manhattan_distance
    )
    
    # 3. Print the results
    if final_path:
        print("✅ Solution Found!")
        for i, state in enumerate(final_path):
            print_board(state, i)
        
        # The number of moves is the length of the path minus one (for the initial state)
        total_moves = len(final_path) - 1
        print(f"Total number of moves needed: {total_moves}")
    else:
        print("❌ No solution found.")


    #  solvable puzzle example:
    # initial:
    #     1,8,2
    #     0,4,3
    #     7,6,5

    #     goal:
    #     1,2,3
    #     4,5,6
    #     7,8,0

# # Main execution (Mindanao cities example)

# if __name__ == "__main__":
#     # Define initial and goal states
#     initial_state = "Davao City"
#     goal_state = "Butuan"

#     # The state space represents the graph of cities and road distances in kilometers.
#     state_space = {
#         'Davao City': {'Tagum': 55, 'Malaybalay': 160, 'General Santos': 150},
#         'Tagum': {'Davao City': 55, 'Butuan': 230},
#         'Malaybalay': {'Davao City': 160, 'Cagayan de Oro': 90},
#         'General Santos': {'Davao City': 150},
#         'Butuan': {'Tagum': 230, 'Cagayan de Oro': 175, 'Surigao': 125},
#         'Cagayan de Oro': {'Malaybalay': 90, 'Butuan': 175, 'Zamboanga City': 400},
#         'Surigao': {'Butuan': 125},
#         'Zamboanga City': {'Cagayan de Oro': 400}
#     }

#     # Heuristic function: straight-line distance (dummy values for illustration)
#     heuristic = {
#         'Davao City': 200,
#         'Cagayan de Oro': 0,
#         'Tagum': 210,
#         'Malaybalay': 80,
#         'General Santos': 320,
#         'Butuan': 150,
#         'Surigao': 250,
#         'Zamboanga City': 350
#     }


#     print("--- A* Algorithm Simulation (Mindanao, Philippines) ---")
#     print(f"Finding the shortest driving route from {initial_state} to {goal_state}...")

#     # Run A* search
#     final_path, final_cost = a_star_search(initial_state, goal_state, state_space, heuristic)

#     # Print the result
#     if final_path:
#         print("\n✅ Path found!")
#         print(f"   Path: {' -> '.join(final_path)}")
#         print(f"   Total Cost (Distance): {final_cost} km")
#     else:
#         print("No path found.")