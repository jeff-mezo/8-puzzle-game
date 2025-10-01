# The goal state of the puzzle, for comparison
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, " "]]

# The initial state of the puzzle
#state = ([[" ", 2, 3], [1, 4, 5], [7, 8, 6]])

state = input("Enter the initial state row-wise, use space for empty tile (e.g., '1 2 3 4 5 6 7 8 '): ")
state = state.split(",")
state = [state[i:i + 3] for i in range(0, len(state), 3)]
# print(state)
# print(str(goal_state))

for i in range(len(goal_state)):
    for j in range(len(goal_state[i])):
        if isinstance(goal_state[i][j], int):
            goal_state[i][j] = str(goal_state[i][j])


while True:

    # print(state[0][0])
    # 1. Display the current state of the board.
    # Loop through the rows and columns to print the grid.
    print("Initial State:")
    for row in state:
        print(" ".join(str(x) for x in row))
    print()  # Print a newline for better readability
    # You can also add clear screen functionality here for a cleaner display.

    print("Goal State:")
    for row in goal_state:
        print(" ".join(str(x) for x in row))
    print()

    if (state) == (goal_state):
        print("Congratulations! You've solved the puzzle!")
        break
    # 2. Check if the current state matches the goal state.
    # If state == goal_state, the puzzle is solved.
    # Print a win message and use a 'break' statement to exit the loop.

    # 3. Get user input for the next move (e.g., 'W', 'A', 'X', 'D').
    # You can use a function like input() to get the player's choice.
    move = input("Enter your move (W/A/S/D): ").upper()

    # 4. Find the coordinates of the empty tile (the number 0).
    # You will need to loop through the 2D list to find where '0' is located.
    empty_tile_row, empty_tile_col = next((r, c) for r in range(3) for c in range(3) if state[r][c] == " ")
    #print(empty_tile_row, empty_tile_col)
    # Store these coordinates (row, col).

    # 5. Determine the new coordinates based on the user's move.
    # For example, if the move is 'W', the new row will be old_row - 1.
    if move == "W":
        new_row, new_col = empty_tile_row - 1, empty_tile_col
    elif move == "A":
        new_row, new_col = empty_tile_row, empty_tile_col - 1
    elif move == "S":
        new_row, new_col = empty_tile_row + 1, empty_tile_col
    elif move == "D":
        new_row, new_col = empty_tile_row, empty_tile_col + 1
    else:
        print("Invalid move. Please enter W, A, S, or D.")
        continue

    print(empty_tile_row, empty_tile_col)
    print(new_row, new_col)

    # 6. Validate the move.
    # Check if the new coordinates are within the board boundaries (0-2 for both row and col).
    if not (0 <= new_row < 3 and 0 <= new_col < 3):
        print("Move out of bounds. Try again.")
        continue
    # If the move is invalid, print an error message and continue the loop.
    # if (new_row, new_col) == (empty_tile_row, empty_tile_col):
    #     print("Invalid move. Try again.")
    #     continue

    # 7. Perform the move by swapping the tiles.
    # Use the coordinates to swap the empty tile ('0') with the tile at the new position.
    state[empty_tile_row][empty_tile_col], state[new_row][new_col] = state[new_row][new_col], state[empty_tile_row][empty_tile_col]

    # Example: state[new_row][new_col], state[old_row][old_col] = state[old_row][old_col], state[new_row][new_col]

    # 8. If the puzzle is not solved, the loop will repeat,
    # displaying the updated board and asking for the next move.
    