# file: eight_puzzle_game.py
# Simple 8-Puzzle sliding game

def instructions():
    # Show game instructions and controls
    print("8-Puzzle Game Start")
    print("The 8-puzzle is a 3x3 board with 8 tiles and one empty space.")
    print("Goal: Reach [[1, 2, 3], [4, 5, 6], [7, 8, ' ']]")
    print("\nRules:")
    print("1. Input the initial state as: 1,2,3,4,5, ,6,7,8")
    print("   (use space for the empty tile)")
    print("2. Moves:")
    print("   'W' → Up, 'S' → Down, 'A' → Left, 'D' → Right")
    print("3. Try to match the goal state.\n")


def display_state(current_state, goal_state):
    #Print current and goal states
    print("\nCurrent State:")
    for row in current_state:
        print(" ".join(row))
    print("\nGoal State:")
    for row in goal_state:
        print(" ".join(row))
    print()


def find_blank(board_state):
    #Find the row, col of the empty tile
    for row_index in range(3):
        for col_index in range(3):
            if board_state[row_index][col_index] == " ":
                return row_index, col_index
    return None


def is_valid_position(row_index, col_index):
    #Check if position is inside the 3x3 grid
    return 0 <= row_index < 3 and 0 <= col_index < 3


def is_valid_action(board_state, move_direction):
    #Check if move is valid for current empty tile
    empty_position = find_blank(board_state)
    if empty_position is None:
        return False

    row_index, col_index = empty_position
    if move_direction == "W": return is_valid_position(row_index - 1, col_index)
    if move_direction == "S": return is_valid_position(row_index + 1, col_index)
    if move_direction == "A": return is_valid_position(row_index, col_index - 1)
    if move_direction == "D": return is_valid_position(row_index, col_index + 1)
    return False


def make_move(board_state, move_direction):
    #Execute move if valid
    if not is_valid_action(board_state, move_direction):
        return board_state, False

    empty_row, empty_col = find_blank(board_state)

    if move_direction == "W": new_row, new_col = empty_row - 1, empty_col
    if move_direction == "S": new_row, new_col = empty_row + 1, empty_col
    if move_direction == "A": new_row, new_col = empty_row, empty_col - 1
    if move_direction == "D": new_row, new_col = empty_row, empty_col + 1

    # Swap empty tile with neighbor
    board_state[empty_row][empty_col], board_state[new_row][new_col] = (
        board_state[new_row][new_col],
        board_state[empty_row][empty_col],
    )

    return board_state, True


def parse_input(user_input):
    #Convert user input into 3x3 state
    tiles = [tile.strip() for tile in user_input.split(",")]
    if len(tiles) != 9:
        raise ValueError("Must have 9 tiles separated by commas")

    normalized_tiles = [" " if tile == "" or tile == " " else tile for tile in tiles]

    if normalized_tiles.count(" ") != 1:
        raise ValueError("Must contain exactly ONE blank space")

    required_tiles = set([str(i) for i in range(1, 9)] + [" "])
    if set(normalized_tiles) != required_tiles:
        raise ValueError("Must contain numbers 1–8 and one blank space")

    return [normalized_tiles[i:i + 3] for i in range(0, 9, 3)]


def main():
    #Run the program
    goal_state = [["1", "2", "3"],
                  ["4", "5", "6"],
                  ["7", "8", " "]]

    instructions()

    try:
        user_input = input("Enter initial state (e.g. '1,2,3,4,5, ,6,7,8'): ")
        current_state = parse_input(user_input)
    except Exception as error:
        print("Error:", error)
        return

    move_count = 0

    while True:
        display_state(current_state, goal_state)

        if current_state == goal_state:
            print(f"Congratulations! You solved it in {move_count} moves!")
            break

        move_direction = input("Enter move (W/A/S/D or Q to quit): ").upper()
        if move_direction == "Q":
            print("Game exited.")
            break

        current_state, move_successful = make_move(current_state, move_direction)
        if move_successful:
            move_count += 1
        else:
            print("Invalid move. Try again.")


if __name__ == "__main__":
    main()
