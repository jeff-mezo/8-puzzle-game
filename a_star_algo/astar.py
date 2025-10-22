import heapq # For implementing priority queue without manual sorting

initial_state = []
goal_state = []
state_space = {}

class Node:
    def __init__(self, state, parent=None, g_cost=0, h_cost=0):
        self.state = state
        self.parent = parent
        self.g_cost = g_cost  # Cost from start to current node
        self.h_cost = h_cost  # Heuristic cost from current node to goal
        self.f_cost = g_cost + h_cost  # Total cost

    def __lt__(self, other):
        return self.f_cost < other.f_cost

def a_star_search(initial_state, goal_state, state_space, heuristic):
    """
    Performs the A* search to find the shortest path from an initial state
    to a goal state.
    """
    open_list = [] # priority queue for nodes to explore
    closed_list = set() # explored nodes

    start_node = Node(state=initial_state, g_cost=0, h_cost=heuristic[initial_state]) # starting node
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
            cost = current_node.g_cost
            temp = current_node
            while temp:
                path.append(temp.state)
                temp = temp.parent
            return path[::-1], cost

        # Explore neighbors
        for neighbor, cost in state_space.get(current_node.state, {}).items():
            if neighbor in closed_list:
                continue

            g_cost = current_node.g_cost + cost # cost from start to neighbor
            h_cost = heuristic[neighbor] # heuristic cost from neighbor to goal
            
            neighbor_node = Node(state=neighbor, parent=current_node, g_cost=g_cost, h_cost=h_cost) # create neighbor node
            heapq.heappush(open_list, neighbor_node) # add neighbor to open list

    return None, 0 # return None if no path is found

# Main execution (Mindanao cities example)

if __name__ == "__main__":
    # Define initial and goal states
    initial_state = "Davao City"
    goal_state = "Butuan"

    # The state space represents the graph of cities and road distances in kilometers.
    state_space = {
        'Davao City': {'Tagum': 55, 'Malaybalay': 160, 'General Santos': 150},
        'Tagum': {'Davao City': 55, 'Butuan': 230},
        'Malaybalay': {'Davao City': 160, 'Cagayan de Oro': 90},
        'General Santos': {'Davao City': 150},
        'Butuan': {'Tagum': 230, 'Cagayan de Oro': 175, 'Surigao': 125},
        'Cagayan de Oro': {'Malaybalay': 90, 'Butuan': 175, 'Zamboanga City': 400},
        'Surigao': {'Butuan': 125},
        'Zamboanga City': {'Cagayan de Oro': 400}
    }

    # Heuristic function: straight-line distance (dummy values for illustration)
    heuristic = {
        'Davao City': 200,
        'Cagayan de Oro': 0,
        'Tagum': 210,
        'Malaybalay': 80,
        'General Santos': 320,
        'Butuan': 150,
        'Surigao': 250,
        'Zamboanga City': 350
    }


    print("--- A* Algorithm Simulation (Mindanao, Philippines) ---")
    print(f"Finding the shortest driving route from {initial_state} to {goal_state}...")

    # Run A* search
    final_path, final_cost = a_star_search(initial_state, goal_state, state_space, heuristic)

    # Print the result
    if final_path:
        print("\n✅ Path found!")
        print(f"   Path: {' -> '.join(final_path)}")
        print(f"   Total Cost (Distance): {final_cost} km")
    else:
        print("No path found.")